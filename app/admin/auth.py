from typing import Optional, Union
from app.logger import logger

from fastapi.responses import RedirectResponse
from fastapi.requests import Request

from sqladmin.authentication import AuthenticationBackend

from app.services.auth import authenticate_user, create_access_token, get_current_user
from app.api.exceptions import UserIsNotAdminException


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        telegram_id, password = form["username"], form["password"]

        user = await authenticate_user(telegram_id, password)
        if user:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"access_token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Union[Optional[RedirectResponse], bool]:
        token = request.session.get("access_token")

        if not token:
            return RedirectResponse(url=request.url_for("admin:login"), status_code=302)

        try:
            user = await get_current_user(token)
            logger.debug(f"Authenticated user: {user}")
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return RedirectResponse(url=request.url_for("admin:login"), status_code=302)

        if user and user.is_admin:
            return True
        else:
            raise UserIsNotAdminException


authentication_backend = AdminAuth(secret_key="...")
