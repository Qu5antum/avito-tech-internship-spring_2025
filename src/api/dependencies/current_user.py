from fastapi import Depends
from sqlalchemy import select

from src.database.db import AsyncSession, get_session
from src.database.models import User
from src.api.schemas.token_schema import TokenPayload
from src.auth.jwt_handler import JWTHandler
from src.auth.jwt_bearer import CurrentUser
from src.exception_handlers.user_exceptions import UserNotFoundException

jwt_handler = JWTHandler()

async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: TokenPayload = Depends(CurrentUser(jwt_handler=jwt_handler))
):
    result = await session.execute(
        select(User).where(User.id == token.sub)
    )

    user = result.scalar_one_or_none()
    
    if not user:
        raise UserNotFoundException("Пользователь не найден.")
    
    return user
