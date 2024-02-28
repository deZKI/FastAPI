from fastapi import APIRouter

router_auth = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)
