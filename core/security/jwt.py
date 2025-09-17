from datetime import datetime, timedelta, timezone
from typing import Union
from jose import jwt, JWTError
from core.config import get_settings

settings = get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    create_access_token

    function to create a token for user returning a jwt token.

    parameters:
    - data (dict): user data received.
    - expires_delta (timedelta): expires date for token

    return:
    - jwt encoded
    """
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """
    decoded_access_token

    decode token received and return users data

    parameters:
    - token (str): the token encoded

    return:
    - if success return user data
    - if not success return None
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
