from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')   # Selecting the hasing algorithm - bcrypt

def hash(password: str):
    return pwd_context.hash(str)