from sqlalchemy.exc import IntegrityError
import logging

from src.database.db import AsyncSession
from src.exception_handlers.db_exception import DatabaseException
from src.repositories.pvz_repository import PVZReposotory
from src.api.schemas.pvz_schema import PVZCreate, PVZOut

logger = logging.getLogger(__name__)

class PVZService:
    def __init__(self, session: AsyncSession) -> dict[PVZOut]:
        self.session = session
        self.pvz_repo = PVZReposotory(session=session)

    async def get_pvzs(self):
        pvzs = await self.pvz_repo.get_all()
        logger.info(
            "PVZ's successfully returned"
        )
        return pvzs

    async def create_pvz(self, data: PVZCreate):
        try:
            new_pvz = await self.pvz_repo.create(
                city=data.city
            )
        
        except IntegrityError:
            logger.error(
                "Database insert failed",
                exc_info=True,
                extra={"City": data.city}
            )
            raise DatabaseException("Ошибка в базе.")
        
        logger.info(
            "PVZ Successully inserted in db",
            extra={"City": data.city}
        )
        
        return new_pvz

        

