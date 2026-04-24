from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from src.database.models import Status


class PVZReceptionCreate(BaseModel):
    pvz_id: UUID
    status: Status


class PVZReceptionOut(PVZReceptionCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True