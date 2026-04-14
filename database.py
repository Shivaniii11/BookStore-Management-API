from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:1111@localhost/bookstore"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)