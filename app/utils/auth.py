from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
import os

# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#  OAuth2 scheme (for authentication)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict):
    """
    Creates a JWT token without expiration.
    """
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hashed version.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password before storing it in the database.
    """
    return pwd_context.hash(password)


# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#  Add `get_current_user`


def get_current_user(token: str = Security(oauth2_scheme)):
    """
    Decodes JWT and returns user information.
    """
    credentials_exception = HTTPException(
        status_code=401, detail="Invalid credentials")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return {"username": username}
