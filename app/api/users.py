from fastapi import APIRouter

from app.schemas.users import SUserRegistration, SUserAuth

router_auth = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router_auth.post("/registration/")
async def register_user(user: SUserRegistration):
    pass

@router_auth.post("/login")
async def auth_user(user: SUserAuth):
    pass

@router_users.get("/{user_id}")
async def get_user(user_id: int):
    pass

