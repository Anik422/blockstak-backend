from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import config



def authenticate_client(client_id: str, client_secret: str):
    if client_id == config.CLIENT_ID and client_secret == config.CLIENT_SECRET:
        return True
    return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(...)):
     # Later we'll fill this part for protected routes
    pass