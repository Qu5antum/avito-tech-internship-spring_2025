from sqlalchemy import delete, select
from uuid import UUID

from .base_repository import BaseRepository
from src.database.models import Product


class ProductRepository(BaseRepository):
    model = Product

    async def delete_with_LIFO(self, reception_id: UUID):
        result = await self.session.execute(
            select(self.model)
            .where(self.model.reception_id == reception_id)
            .order_by(self.model.created_at.desc())
            .limit(1)
        )

        instance = result.scalar_one_or_none()

        if not instance:
            return None

        await self.session.delete(instance=instance)
        await self.session.commit()

        return instance