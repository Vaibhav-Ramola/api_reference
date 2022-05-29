from .database import Base          # the Base model is must import from the database.py file
from sqlalchemy import TIMESTAMP, Column, String, Integer, Boolean, text
# models represent tables
# These are SQL Alchemy models that defines how our specific tables look like in our database
# Each class that we use to define our models must extend Base 
class Post(Base):
    # table name
    __tablename__ = 'posts'

    # creating columns for the table
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = 'users'

    #creating the columns for the table
    id = Column(Integer, nullable=False, primary_key=True)
    # username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at =Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))