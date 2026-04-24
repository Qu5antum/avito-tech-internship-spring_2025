from sqlalchemy.exc import IntegrityError

from src.database.db import AsyncSession
from src.exception_handlers.db_exception import DatabaseException
from src.repositories.pvz_repository import PVZReposotory
from src.api.schemas.pvz_schema import PVZCreate


class PVZService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.pvz_repo = PVZReposotory(session=session)

    async def get_pvzs(self):
        return await self.pvz_repo.get_all()

    async def create_pvz(self, data: PVZCreate) -> dict:
        try:
            new_pvz = await self.pvz_repo.create(
                city=data.city
            )
        
        except IntegrityError:
            raise DatabaseException("Ошибка в базе.")
        
        return {
            "detail": "ПВЗ успешно создано.",
            "pvz": new_pvz
        }

        

