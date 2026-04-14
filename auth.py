from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import SessionLocal
import models, utils

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ REGISTER (FORM INPUTS)
@router.post("/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form("user"),
    db: Session = Depends(get_db)
):
    hashed = utils.hash_password(password)

    new_user = models.User(
        name=name,
        email=email,
        password=hashed,
        role=role
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered"}

# ✅ LOGIN (FORM INPUTS)
@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not utils.verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = utils.create_token({
        "user_id": user.id,
        "role": user.role
    })

    return {"access_token": token}