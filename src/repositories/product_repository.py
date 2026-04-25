from .base_repository import BaseRepository

from src.database.models import Product


class ProductRepository(BaseRepository):
    model = Product