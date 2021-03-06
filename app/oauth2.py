from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from .config import settings
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# You need to provide:
# SECRET KEY
# ALGORITHM
# EXPIRATION_DATE

SECRET_KEY = f'{settings.secret_key}'
ALGORITHM = f'{settings.algorithm}'         # the algorithm that will be used
EXPIRATION_TIME = f'{settings.access_token_expire_minutes}'            # In minutes

def create_access_token(data: dict):            # function to create access token
    encode = data.copy()
    expiration_time = datetime.utcnow() + timedelta(minutes=30)
    
    encode.update({"exp": expiration_time})   
    # Updates the payload with token expiration time
    encoded = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    # Creates the token using the given SECRET_KEY and ALGORITHM
    return encoded

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})

    return verify_access_token(token=token, credentials_exception=credentials_exception)