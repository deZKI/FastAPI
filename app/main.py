from fastapi import FastAPI

from app.api.users import router_auth, router_users


app = FastAPI(docs_url='/api/swagger/')
app.include_router(router_users)
app.include_router(router_auth)
