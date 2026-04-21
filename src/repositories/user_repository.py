from sqlalchemy import select

from .base_repository import BaseRepository
from database.models import User


class UserRepository(BaseRepository):
    model = User

    async def get_user_with_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )

        existing_user = result.scalar_one_or_none()

        return existing_user