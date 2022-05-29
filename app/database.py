from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Format : ''postgresql://<username>:<password>@<ip-address/hostname>/<database_name>''
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:vaibhav92002@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)         # connects us to the database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)     # A session is required to start talking to the database

Base = declarative_base()       # All the models that we will use to describe, how we sent and receive data
# from out database must extend this class
# check models.py file


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 