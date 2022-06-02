from .database import Base          # the Base model is must import from the database.py file
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Integer, Boolean, text
from sqlalchemy.orm import relationship
# models represent tables
# These are SQL Alchemy models that defines how our specific tables look like in our database
# Each class that we use to define our models must extend Base 
class Post(Base):
    # table name
    __tablename__ = 'posts'

    # creating columns for the table
    id = Column(Integer, primary_key=True, nullable=False)          # setting id as the primary key
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)      # Establishes a foreign key between 'users' and 'posts' table

    owner = relationship('User')            # creating a relation that relates two tables 

class User(Base):
    __tablename__ = 'users'

    #creating the columns for the table
    id = Column(Integer, nullable=False, primary_key=True)      # setting id as the primary key
    # username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at =Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE', primary_key=True))