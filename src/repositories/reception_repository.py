from sqlalchemy import select
from uuid import UUID
from typing import Optional

from .base_repository import BaseRepository
from src.database.models import Reception
from src.database.models import Status


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