from fastapi import HTTPException, status


class UserAlreadyExistsException(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"
