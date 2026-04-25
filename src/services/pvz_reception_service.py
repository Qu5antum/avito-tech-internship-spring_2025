from sqlalchemy.exc import IntegrityError
from uuid import UUID
from typing import Optional

from src.database.db import AsyncSession
from src.database.models import Reception
from src.repositories.reception_repository import ReceptionRepository
from src.repositories.pvz_repository import PVZReposotory
from src.api.schemas.reception_schema import PVZReceptionCreate
from src.exception_handlers.pvz_exception import PVZNotFoundException
from src.exception_handlers.reception_exception import ReceptionStatusException
from src.exception_handlers.db_exception import DatabaseException
from src.database.models import Status


class PVZReceptionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.reception_repo = ReceptionRepository(session=session)
        self.pvz_repo = PVZReposotory(session=session)


    async def create_reception(self, reception: PVZReceptionCreate) -> dict:
        existing_pvz = await self.pvz_repo.get(id=reception.pvz_id)

        if not existing_pvz:
            raise PVZNotFoundException("ПВЗ Не Найдено.")
        
        reception_status = await self.reception_repo.get_reception_status(pvz_id=reception.pvz_id)

        if reception_status:
            raise ReceptionStatusException("Приемка товаров открыта у этого ПВЗ, вы не можете создать новый.")
        
        try:
            new_reception = await self.reception_repo.create(
                pvz_id=reception.pvz_id,
                status=reception.status
            )

        except IntegrityError:
            raise DatabaseException("Ошибка в базе.")
        
        return {
            "detail": "Приемка товаров успешно создано",
            "reception": new_reception
        }
    
    async def close_reception(self, pvz_id: UUID) -> Optional[Reception]:
        existing_pvz = await self.pvz_repo.get(id=pvz_id)

        if not existing_pvz:
            raise PVZNotFoundException("ПВЗ Не Найдено.")
        
        reception = await self.reception_repo.get_reception_status(pvz_id=pvz_id)

        if not reception:
            raise ReceptionStatusException("Приемка товаров уже закрыта у этого ПВЗ.")
        
        reception.status = Status.CLOSE
        await self.session.commit()
        await self.session.refresh(reception)

        return reception
        



