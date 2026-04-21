from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from datetime import datetime

from .jwt_handler import JWTHandler
from src.api.schemas.token_schema import TokenPayload



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/login")

class CurrentUser:
    def __init__(self, jwt_handler: JWTHandler):
        self.jwt_handler = jwt_handler

    def __call__(self, token: str = Depends(oauth2_scheme)) -> TokenPayload:
        try:
            payload = self.jwt_handler.decode_token(token)
            token_data = TokenPayload(**payload)

            if token_data.token_type != "access":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return token_data

        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )