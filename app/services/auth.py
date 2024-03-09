from datetime import datetime, timedelta
from typing import Optional
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends, Request

from app.config import settings
from app.database.dao import UsersDAO
from app.api.exceptions import (IncorrectTelegramIdOrPasswordException, TokenAbsentException,
                                TokenExpiredException, UserIsNotPresentException, IncorrectTokenFormatException)

# Настройки
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(telegram_id: int, password: str):
    user = await UsersDAO.find_one_or_none(telegram_id=telegram_id)
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectTelegramIdOrPasswordException
    return user


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, ALGORITHM
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
