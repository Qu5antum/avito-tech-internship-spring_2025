from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from src.database.models import ProductType


class ProductCreate(BaseModel):
    type: ProductType
    reception_id: UUID


class Productout(ProductCreate):
    id: UUID
    created_at: datetime