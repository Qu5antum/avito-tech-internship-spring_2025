from sqlalchemy.exc import IntegrityError
from uuid import UUID
from typing import Optional
from datetime import datetime
import logging

from src.database.db import AsyncSession
from src.database.models import Reception
from src.repositories.reception_repository import ReceptionRepository
from src.repositories.pvz_repository import PVZReposotory
from src.api.schemas.reception_schema import PVZReceptionCreate
from src.exception_handlers.pvz_exception import PVZNotFoundException
from src.exception_handlers.reception_exception import ReceptionStatusException
from src.exception_handlers.db_exception import DatabaseException
from src.database.models import Status

logger = logging.getLogger(__name__)

class PVZReceptionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.reception_repo = ReceptionRepository(session=session)
        self.pvz_repo = PVZReposotory(session=session)


    async def create_reception(self, reception: PVZReceptionCreate) -> dict:
        existing_pvz = await self.pvz_repo.get(id=reception.pvz_id)

        if not existing_pvz:
            logger.warning(
                "PVZ Not Found",
                extra={"pvz_id": str(reception.pvz_id)}
            )
            raise PVZNotFoundException("ПВЗ Не Найдено.")
        
        reception_status = await self.reception_repo.get_reception_status(pvz_id=reception.pvz_id)

        if reception_status:
            logger.warning(
                "Reception in this PVZ is in_progress",
                extra={"pvz_id": str(reception.pvz_id)}
            )
            raise ReceptionStatusException("Приемка товаров открыта у этого ПВЗ, вы не можете создать новый.")
        
        try:
            new_reception = await self.reception_repo.create(
                pvz_id=reception.pvz_id,
                status=reception.status
            )

        except IntegrityError:
            logger.error(
                "Database insert error",
                exc_info=True,
                extra={"pvz_id": str(reception.pvz_id)}
            )
            raise DatabaseException("Ошибка в базе.")
        
        logger.info(
            "Reception Successully inserted in db",
            extra={"reception_status": reception.status}
        )

        return {
            "detail": "Приемка товаров успешно создано",
            "reception": new_reception
        }
    
    async def close_reception(self, pvz_id: UUID) -> Optional[Reception]:
        existing_pvz = await self.pvz_repo.get(id=pvz_id)

        if not existing_pvz:
            logger.warning(
                "PVZ Not Found",
                extra={"pvz_id": str(reception.pvz_id)}
            )
            raise PVZNotFoundException("ПВЗ Не Найдено.")
        
        reception = await self.reception_repo.get_reception_status(pvz_id=pvz_id)

        if not reception:
            logger.warning(
                "Reception in this PVZ is closed",
                extra={"pvz_id": str(reception.pvz_id)}
            )
            raise ReceptionStatusException("Приемка товаров уже закрыта у этого ПВЗ.")
        
        reception.status = Status.CLOSE
        await self.session.commit()
        await self.session.refresh(reception)
        
        logger.info(
            "Status successfully updated",
            extra={"status": reception.status}
        )
        
        return reception
    
    async def reception_detail(
        self, 
        pvz_id: UUID,
        from_date: datetime | None = None,
        to_date: datetime | None = None
    ):
        existing_pvz = await self.pvz_repo.get(id=pvz_id)

        if not existing_pvz:
            logger.warning(
                "PVZ Not Found",
                extra={"pvz_id": str(pvz_id)}
            )
            raise PVZNotFoundException("ПВЗ Не Найдено.")
        
        reception_with_products = await self.reception_repo.get_filtered_reception(
            pvz_id=pvz_id,
            from_date=from_date,
            to_date=to_date
        )

        logger.info(
            "Successfully receptions info returned",
            extra={"pvz_id": str(pvz_id)}
        )

        return reception_with_products
        




