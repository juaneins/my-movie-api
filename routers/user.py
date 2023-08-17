from pydantic import BaseModel
from jwt_manager import create_token
from fastapi.responses import JSONResponse
from fastapi import APIRouter

user_router = APIRouter()


class User(BaseModel):
    email: str
    password: str


@user_router.post('/login', tags=['auth'])
def login(user: User):
    if (user.email == "admin@mail.com" and user.password == "secret"):
        token: str = create_token(user.model_dump())
        return JSONResponse(content=token)