from email.policy import default
from turtle import title
from .database import Base          # the Base model is must import from the database.py file
from sqlalchemy import Column, String, Integer, Boolean


# Each class that we use to define our models must extend Base 
class Post(Base):
    # table name
    __tablename__ = 'Posts'

    # creating columns for the table
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)