from pydantic import BaseModel


class SUser(BaseModel):
    """ Схема пользователей"""
    name: str
    surname: str
    telegram_id: str
    has_know_from: str
    church: str
    is_admin: bool = False


class SUserRegistration(BaseModel):
    """  Схема регистрации пользователя """
    name: str
    surname: str
    password: str
    telegram_id: str
    has_know_from: str
    church: str


class SUserAuth(BaseModel):
    """ Схема входа"""
    telegram_id: str
    password: str
