from fastapi import FastAPI
from sqladmin import Admin

from app.api.users import router_auth, router_users
from app.database.connection import engine
from app.admin.auth import authentication_backend
from app.admin.views import UsersAdmin

app = FastAPI(docs_url='/api/swagger/')
app.include_router(router_users)
app.include_router(router_auth)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
