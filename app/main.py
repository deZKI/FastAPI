import datetime

from fastapi import FastAPI, Cookie, Response
from fastapi.responses import FileResponse

from .models.users import User
app = FastAPI(docs_url='/api/swagger/')


@app.get("/")
async def root():
    return FileResponse('templates/index.html')

@app.post("/users")
async def users(user: User):
    response = User(**user.model_dump())
    return response

@app.post("/calculate/{user_id}")
async def calculate(user_id: int, num1: int, num2: int):
    return {'result': num1 + num2}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/items/")
async def read_items(response: Response):
    now = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")  # получаем текущую дату и время
    response.set_cookie(key="last_visit", value=now)
    return {"message": "куки установлены"}