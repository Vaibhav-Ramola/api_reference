from typing import List, Optional
from fastapi import Depends, status, APIRouter
from fastapi import HTTPException
from sqlalchemy.orm import Session                  # important
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter()

@router.get('/sqlalchemy')
def test_fun(db: Session = Depends(get_db)):        
    # to do any database operations we must pass 'db: Session = Depends(get_db)'
    # to the function, when using sqlalchemy or any other orm
    # it opens a Session to perform the operations and then closes it when we are done
    posts = db.query(models.Post).all()
    # models represent tables
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not resolve the query')

    return {"data": posts}                      
                                                    
# @router.get('/posts', response_model=List[schemas.Post])          # decorator to fetch data from the database
# to receive list of Post types
@router.get('/posts', response_model=List[schemas.PostOut])
async def post(db:Session = Depends(get_db), limit:int = 10, skip:int = 0, search: Optional[str] = ''):  # Added limit query parameter
    # query parameters are passsed as function arguments like above function
    # # Using SQL query
    # cursor.execute('SELECT * FROM posts')
    # posts = cursor.fetchall()

    #using  sqlalchemy

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  # to generate query to fetch all table content
    # added query parameters of         search                                  limit           skip
    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    print(posts)
    return results

@router.post('/posts', response_model=schemas.Post)              # decorator to post data to the database
async def create_post(payload: schemas.PostCreat, db:Session = Depends(get_db), user_id: schemas.TokenData = Depends(oauth2.get_current_user)):          # payload is stored as a pydantic model
    # # Using SQL query

    # # the 'RETURNING *' query at the end of the query statement is important or the server throws error
    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', (payload.title, payload.content, payload.published))          # Don't use string f-strings, prone to SQL-injections
    # post  = cursor.fetchone()
    # connection.commit()             # It's important to commit, to push all the changes to the database otherwise the changes won't be reflected in the database
    
    # created_post = models.Post(title=payload.title, content=payload.content, published=payload.published)       # new post created
    # An efficient routerroach
    created_post = models.Post(owner_id=user_id.id, **payload.dict())       # due to post being a pydantic model
    db.add(created_post)        # adding the post to database
    db.commit()                 # commiting the changes to database
    db.refresh(created_post)    # return the newly created and stores it in created_post
    print(created_post)
    # print(payload.dict())                     # Every pydantic model has a .dict() function to convert it to a dictionary
    return created_post

@router.get('/posts/{id}', response_model=schemas.Post)
async def get_post_by_id(id: int, db:Session = Depends()):
    # SQL method
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''', str(id))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        # Raise an HTTP exception if the post is null and send the routerropriate message
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not find post with id : {id}')
    return post

@router.delete('/posts/{id}', response_model=schemas.Post)          # decorator to delete data from database
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

@router.put('/posts/{id}', response_model=schemas.Post)             # decorator to Update data in the database
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
