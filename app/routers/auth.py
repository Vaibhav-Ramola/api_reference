from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, schemas, utils, models, oauth2

router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(user_creds: schemas.UserLogin,db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(user_creds.email == models.User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')

    access_token = oauth2.create_access_token(data={"user_id": user_creds.id})
    return {"access_token": access_token, "token": "bearer"}