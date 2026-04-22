from pydantic import BaseModel, EmailStr
from uuid import UUID
import datetime

from src.database.models import UserRole


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: UserRole


class UserOut(UserBase):
    id: UUID
    created_at: datetime.datetime
    
    class Config:
        from_attributes = True
    
    