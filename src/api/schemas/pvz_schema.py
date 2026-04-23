from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from src.database.models import AllowedCities


class PVZCreate(BaseModel):
    city: AllowedCities

class PVZOut(PVZCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True