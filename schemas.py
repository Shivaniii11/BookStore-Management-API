from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "user"

class LoginSchema(BaseModel):
    email: str
    password: str

class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    stock: int

class OrderItem(BaseModel):
    book_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]