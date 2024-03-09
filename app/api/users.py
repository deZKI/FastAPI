from fastapi import APIRouter, Response, Depends

from app.schemas.users import SUserRegistration, SUserAuth, SUser
from app.database.dao import UsersDAO
from app.api.exceptions import UserAlreadyExistsException, CannotAddDataToDatabase
from app.services.auth import get_password_hash, authenticate_user, create_access_token, get_current_user

router_auth = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router_auth.post("/register", status_code=201)
async def register_user(user_data: SUserRegistration):
    existing_user = await UsersDAO.find_one_or_none(telegram_id=user_data.telegram_id)
    if existing_user:
        raise UserAlreadyExistsException
    plain_password = user_data.password.get_secret_value()
    hashed_password = get_password_hash(plain_password)
    new_user = await UsersDAO.add_with_qr_code(telegram_id=user_data.telegram_id, name=user_data.name,
                                               surname=user_data.surname,
                                               church=user_data.church,
                                               age=user_data.age,
                                               hashed_password=hashed_password)
    if not new_user:
        raise CannotAddDataToDatabase


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.telegram_id, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router_users.get("/me")
async def read_users_me(current_user: SUser = Depends(get_current_user)):
    return current_user
