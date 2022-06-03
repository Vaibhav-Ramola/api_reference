import psycopg2
from psycopg2.extras import RealDictCursor          # important, otherwise the library won't give column names only values from the table
import time
from .database import engine
from . import models
from fastapi import FastAPI
from .routers import post, user, auth, votes

models.Base.metadata.create_all(bind=engine)  # Binds the engine and creates the table


while True:         # An infinite loop to keep trying to connect to the database
    try:        # The below code is prone to failure so it is kept in a try catch block
        connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='vaibhav92002', cursor_factory=RealDictCursor)    
        # The last argument is important, to get column names along with the values
        cursor = connection.cursor()     # this will be used to execute SQL statements
        print('Successfully Connected !!!');
        break   # If we successfully are connected then we break out of the loop
    except Exception as error:
        print("Connection Failed")
        print(f'Error : {error}')
        time.sleep(2)       # if we fail to connect the keep trying with 2 sec delay


app = FastAPI()             # Initializing the app
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get('/')
async def root():
    return {"message": "Welcome to my api"}

