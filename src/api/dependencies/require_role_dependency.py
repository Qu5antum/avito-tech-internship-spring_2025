from fastapi import Depends

from .current_user import get_current_user
from src.database.models import User, UserRole
from src.exception_handlers.access_exception import AccessException


def require_moderator(user: User = Depends(get_current_user)):
    if user.role != UserRole.MODERATOR:
        raise AccessException("Доступ запрещен.")
    
    return user

            
            
            
