from fastapi import FastAPI, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
import models
from datetime import date
from typing import Literal

app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# 👤 USER REGISTER (WITH DROPDOWN)
# =========================
@app.post("/user/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: Literal["user", "seller"] = Form(...),  # 🔥 DROPDOWN
    db: Session = Depends(get_db)
):
    # Check duplicate email
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=name,
        email=email,
        password=password,
        role=role
    )

    db.add(new_user)
    db.commit()

    return {"message": f"{role} registered successfully"}

# =========================
# 📚 ADD BOOK (SELLER ONLY)
# =========================
@app.post("/seller/add-product")
def add_product(
    title: str = Form(...),
    author: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    seller_id: int = Form(...),  # 🔥 who is adding
    db: Session = Depends(get_db)
):
    seller = db.query(models.User).filter(models.User.id == seller_id).first()

    if not seller or seller.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can add books")

    book = models.Book(
        title=title,
        author=author,
        price=price,
        stock=stock
    )

    db.add(book)
    db.commit()

    return {"message": "Book added successfully"}

# =========================
# 🛒 BUY BOOK
# =========================
@app.post("/user/buy")
def buy_product(
    user_id: int = Form(...),
    book_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.stock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    total = book.price * quantity
    book.stock -= quantity

    order = models.Order(user_id=user_id, total_price=total)
    db.add(order)
    db.commit()

    return {"message": "Book purchased", "total": total}

# =========================
# 👑 ADMIN DASHBOARD
# =========================
@app.get("/admin/dashboard")
def dashboard(db: Session = Depends(get_db)):

    total_users = db.query(models.User).filter(models.User.role == "user").count()
    total_sellers = db.query(models.User).filter(models.User.role == "seller").count()

    total_books = db.query(models.Book).count()
    total_orders = db.query(models.Order).count()

    total_revenue = db.query(func.sum(models.Order.total_price)).scalar() or 0

    today = date.today()
    today_revenue = db.query(func.sum(models.Order.total_price)).filter(
        func.date(models.Order.created_at) == today
    ).scalar() or 0

    return {
        "total_users": total_users,
        "total_sellers": total_sellers,
        "total_authors": total_sellers,
        "total_books": total_books,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "today_revenue": today_revenue
    }