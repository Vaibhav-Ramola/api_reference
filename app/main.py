from dataclasses import dataclass
from multiprocessing import connection
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor          # important, otherwise the library won't give column names only values from the table
import time


class Post(BaseModel):              # will check if the post request has all these fields or not if not will through error automatucally
    title: str
    body: str
    publish: bool = True            # default value set to True
    rating: Optional[int] = None    # a completely optional field of type int, defaults to a value of none


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

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Welcome to my api"}

@app.get('/post')
async def post():
    return {"message": "This is your get reuqest for post"}

@app.post('/')
async def post_request(payload: Post):          # payload is stored as a pydantic model
    print(payload)
    # print(payload.dict())                     # Every pydantic model has a .dict() function to convert it to a dictionary
    return {"message": f"This is the title of your post request : {payload.title}"}

