from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import Optional
from datetime import datetime

from .base_repository import BaseRepository
from src.database.models import Reception, Status, Product


class ReceptionRepository(BaseRepository):
    model = Reception
    
    async def get_reception_status(self, pvz_id: UUID) -> Optional[Reception]:
        result = await self.session.execute(
            select(self.model)
            .where(
                self.model.pvz_id == pvz_id,
                self.model.status == Status.IN_PROGRESS
            )
        )

        return result.scalar_one_or_none()
    
    async def get_filtered_reception(
        self, 
        pvz_id: UUID, 
        from_date: datetime | None = None, 
        to_date: datetime | None = None
    ):
        query = (
            select(self.model)
            .options(selectinload(self.model.products))
            .where(
                self.model.pvz_id == pvz_id
            )
        ) 
        if from_date:
            query=query.where(Product.created_at >= from_date)
        if to_date:
            query=query.where(Product.created_at <= to_date)

        result = await self.session.execute(query)

        return result.scalars().all()