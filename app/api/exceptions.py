from fastapi import HTTPException, status


class CustomException(HTTPException):

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(CustomException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Пользователь уже существует"


class CannotAddDataToDatabase(CustomException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class TokenAbsentException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED


class UserIsNotAdminException(CustomException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Пользователь не является админом"


class TokenExpiredException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class IncorrectTelegramIdOrPasswordException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная id или пароль"
