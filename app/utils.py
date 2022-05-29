from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')   # Selecting the hasing algorithm - bcrypt

def hash(password: str):
    return pwd_context.hash(password)

def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)        # converts hashes the plain password and compares it to hasded_password