
from .base_repository import BaseRepository
from src.database.models import PVZ


class PVZReposotory(BaseRepository):
    model = PVZ
