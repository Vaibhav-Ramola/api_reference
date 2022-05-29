from fastapi import Depends, APIRouter, status
from fastapi import HTTPException
from sqlalchemy.orm import Session                  # important
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter()

@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):    # Ordering of argument is important, try switching 
    user.password = utils.hash(str(user.password))
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not find user with id: {id}')
    
    return user
