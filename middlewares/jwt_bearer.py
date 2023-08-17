from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jwt_manager import validate_token
from http import HTTPStatus


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if (data["email"] != "admin@mail.com"):
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                                detail="Credenetials are invalid")
