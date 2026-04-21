from typing import Any
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from database.db import AsyncSession
from repositories.user_repository import UserRepository
from exception_handlers.user_exceptions import UserNotFoundException, UnauthorizedException
from auth.utils import check_hashes
from core.config import settings
from auth.jwt_handler import JWTHandler

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session=session)
        self.jwt_handler = JWTHandler()

    async def auth_user(self, credents: OAuth2PasswordRequestForm) -> Any:
        user = await self.user_repository.get_user_with_email(email=credents.username)


        if not user:
            UserNotFoundException("User not found.")
 
        # ДОБАВИТЬ is_active В МОДЕЛЬ USER!!!!!!!!!!
        if not user.is_active:
            return UnauthorizedException("User is unauthorized.")
        
        if not check_hashes(credents.password, user.password):
            return UnauthorizedException("Invalid credentials.")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = self.jwt_handler.create_access_token(
            subject=user.email,
            role=user.role,
            expires_delta=access_token_expires
        )

        refresh_token = self.jwt_handler.create_refresh_token(subject=user.email)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
        



        
        
        