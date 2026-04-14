from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(String(255))
    role = Column(String(10))

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    author = Column(String(255))
    price = Column(Float)
    stock = Column(Integer)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))