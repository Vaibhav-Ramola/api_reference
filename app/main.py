from http.client import HTTPException
from msilib import schema
from multiprocessing import connection
from typing import List
from fastapi import Depends, FastAPI, status
import psycopg2
from psycopg2.extras import RealDictCursor          # important, otherwise the library won't give column names only values from the table
import time
from fastapi import HTTPException
from sqlalchemy.orm import Session                  # important
from . import models, schemas, utils
from .database import engine, get_db


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


@app.get('/')
async def root():
    return {"message": "Welcome to my api"}

@app.get('/sqlalchemy')
def test_fun(db: Session = Depends(get_db)):        
    # to do any database operations we must pass 'db: Session = Depends(get_db)'
    # to the function, when using sqlalchemy or any other orm
    # it opens a Session to perform the operations and then closes it when we are done
    posts = db.query(models.Post).all()
    # models represent tables
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not resolve the query')

    return {"data": posts}                      
                                                    
@app.get('/posts', response_model=List[schemas.Post])          # decorator to fetch data from the database
# to receive list of Post types
async def post(db:Session = Depends(get_db)):
    # # Using SQL query
    # cursor.execute('SELECT * FROM posts')
    # posts = cursor.fetchall()

    #using  sqlalchemy

    posts = db.query(models.Post).all()  # to generate query to fetch all table content
    print(posts)
    return posts

@app.post('/posts', response_model=schemas.Post)              # decorator to post data to the database
async def create_post(payload: schemas.PostBase, db:Session = Depends(get_db)):          # payload is stored as a pydantic model
    # # Using SQL query

    # # the 'RETURNING *' query at the end of the query statement is important or the server throws error
    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', (payload.title, payload.content, payload.published))          # Don't use string f-strings, prone to SQL-injections
    # post  = cursor.fetchone()
    # connection.commit()             # It's important to commit, to push all the changes to the database otherwise the changes won't be reflected in the database
    
    # created_post = models.Post(title=payload.title, content=payload.content, published=payload.published)       # new post created
    # An efficient approach
    created_post = models.Post(**payload.dict())       # due to post being a pydantic model
    db.add(created_post)        # adding the post to database
    db.commit()                 # commiting the changes to database
    db.refresh(created_post)    # return the newly created and stores it in created_post
    print(created_post)
    # print(payload.dict())                     # Every pydantic model has a .dict() function to convert it to a dictionary
    return created_post

@app.get('/posts/{id}', response_model=schemas.Post)
async def get_post_by_id(id: int, db:Session = Depends()):
    # SQL method
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''', str(id))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        # Raise an HTTP exception if the post is null and send the appropriate message
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not find post with id : {id}')
    return post

@app.delete('/posts/{id}', response_model=schemas.Post)          # decorator to delete data from database
async def delete_post_by_id(id: int, db:Session = Depends(get_db)):
    # SQL method
    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))       # That , in the format string is important
    # deleted_post = cursor.fetchone()
    # # Remember to commit the data to the database whenever making changes to the database
    # connection.commit()
    # # print(deleted_post)

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post with id : {id} found')
    deleted_post = post.delete(synchronize_session=False)
    db.commit()
    return deleted_post

@app.put('/posts/{id}', response_model=schemas.Post)             # decorator to Update data in the database
async def update_post_by_id(id: int, post: schemas.PostBase, db:Session = Depends()):
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, publushed = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()
    posts = db.query(models.Post).filter(models.Post.id == id)

    if not posts.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Can not update post with id : {id}')
    posts.update(post.dict(), synchronize_session=False)
    db.commit()
    return posts.first()

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):    # Ordering of argument is important, try switching 
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not find user with id: {id}')
    
    return user
