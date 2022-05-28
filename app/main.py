from http.client import HTTPException
from multiprocessing import connection
from typing import Optional
from fastapi import Depends, FastAPI, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor          # important, otherwise the library won't give column names only values from the table
import time
from fastapi import HTTPException
from sqlalchemy.orm import Session                  # important
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)  # Binds the engine and creates the table


class Post(BaseModel):              # will check if the post request has all these fields or not if not will through error automatucally
    title: str
    content: str
    published: bool = True            # default value set to True
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


app = FastAPI()             # Initializing the app


@app.get('/')
async def root():
    return {"message": "Welcome to my api"}

@app.get('/sqlalchemy')
def test_fun(db: Session = Depends(get_db)):
    return {"test": "Success"}

@app.get('/posts')          # decorator to fetch data from the database
async def post():
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    print(posts)
    return posts

@app.post('/posts')              # decorator to post data to the database
async def post_request(payload: Post):          # payload is stored as a pydantic model
    # the 'RETURNING *' query at the end of the query statement is important or the server throws error
    cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', (payload.title, payload.content, payload.published))          # Don't use string f-strings, prone to SQL-injections
    post  = cursor.fetchone()
    connection.commit()             # It's important to commit, to push all the changes to the database otherwise the changes won't be reflected in the database
    print(post)
    # print(payload.dict())                     # Every pydantic model has a .dict() function to convert it to a dictionary
    return {"data": post}

@app.get('/posts/{id}')
async def get_post_by_id(id: int):
    cursor.execute('''SELECT * FROM posts WHERE id = %s''', str(id))
    post = cursor.fetchone()
    print(post)
    if not post:
        # Raise an HTTP exception if the post is null and send the appropriate message
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not find post with id : {id}')
    return {'post_detail': post}

@app.delete('/posts/{id}')          # decorator to delete data from database
async def delete_post_by_id(id: int):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))       # That , in the format string is important
    deleted_post = cursor.fetchone()
    # Remember to commit the data to the database whenever making changes to the database
    connection.commit()
    # print(deleted_post)
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post with id : {id} found')
    return deleted_post

@app.put('/posts/{id}')             # decorator to Update data in the database
async def update_post_by_id(id: int, post: Post):
    cursor.execute('''UPDATE posts SET title = %s, content = %s, publushed = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    connection.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Can not update post with id : {id}')

    return {'post' : updated_post} 
