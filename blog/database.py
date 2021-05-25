from sqlalchemy import create_engine  # Import sqlalchemy create engine function to create engine to connect database
from sqlalchemy.ext.declarative import declarative_base # create declarative base for defining all your models
from sqlalchemy.orm import sessionmaker # Create database session to enable database communicate with server

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"  # This is a url link to the local database
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True,
                       connect_args={"check_same_thread": True})  # This is the database engine creation

Base = declarative_base()  # This is the base where our models are connected to our database
SessionLocal = sessionmaker(bind=engine, autoflush=False,
                            autocommit=False)  # This is where we create our session with our database


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

