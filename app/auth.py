from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_client(client_id: str, client_secret: str):
    """
    Authenticate the client using client_id and client_secret.
    """
    print(client_id, client_secret, config.CLIENT_ID, config.CLIENT_SECRET)
    if client_id == config.CLIENT_ID and client_secret == config.CLIENT_SECRET:
        return True
    return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Verify the JWT token and return the user.
    """
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )