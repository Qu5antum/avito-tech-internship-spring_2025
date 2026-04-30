from sqlalchemy.exc import IntegrityError
from uuid import UUID
import logging

from src.database.db import AsyncSession
from src.repositories.product_repository import ProductRepository
from src.repositories.pvz_repository import PVZReposotory
from src.repositories.reception_repository import ReceptionRepository
from src.api.schemas.product_schema import ProductCreate
from src.exception_handlers.pvz_exception import PVZNotFoundException
from src.exception_handlers.reception_exception import ReceptionStatusException
from src.exception_handlers.db_exception import DatabaseException
from src.exception_handlers.product_exception import ProductNotFoundException

logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.pvz_repo = PVZReposotory(session=session)
        self.reception_repo = ReceptionRepository(session=session)
        self.product_repo = ProductRepository(session=session)

    async def create_product(self, pvz_id: UUID, product: ProductCreate) -> dict:
        existing_pvz = await self.pvz_repo.get(id=pvz_id)

        if not existing_pvz:
            logger.warning(
                "PVZ Not Found",
                extra={"pvz_id": str(pvz_id)}
            )
            raise PVZNotFoundException("ПВЗ Не Найдено.")
        
        reception_status = await self.reception_repo.get_reception_status(pvz_id=pvz_id)

        if not reception_status:
            logger.warning(
                "Reception in this PVZ is closed",
                extra={"pvz_id": str(pvz_id)}
            )
            raise ReceptionStatusException("Приемка товаров закрыта у этого ПВЗ, вы не можете добавить товар.")
        
        try:
            new_product = await self.product_repo.create(
                type=product.type,
                reception_id=reception_status.id
            )
        
        except IntegrityError:
            logger.error(
                "Database insert error",
                exc_info=True,
                extra={"pvz_id": str(pvz_id)}
            )
            raise DatabaseException("Ошибка в базе.")
        
        logger.info(
            "Database insert success",
            extra={"product": product.type}
        )

        return {
            "detail": "Продукт добавлен",
            "product": new_product
        }

    async def delete_product(self, pvz_id: UUID) -> dict:
        existing_pvz = await self.pvz_repo.get(id=pvz_id)

        if not existing_pvz:
            logger.warning(
                "PVZ Not Found",
                extra={"pvz_id": str(pvz_id)}
            )
            raise PVZNotFoundException("ПВЗ Не Найдено.")
        
        reception_status = await self.reception_repo.get_reception_status(pvz_id=pvz_id)

        if not reception_status:
            logger.warning(
                "Reception in this PVZ is closed",
                extra={"pvz_id": str(pvz_id)}
            )
            raise ReceptionStatusException("Приемка товаров закрыта у этого ПВЗ, вы не можете удалить товар.")
        
        product_to_delete = await self.product_repo.delete_with_LIFO(reception_id=reception_status.id)

        if not product_to_delete:
            logger.warning(
                "Product Not Found",
                extra={"pvz_id": str(pvz_id)}
            )
            raise ProductNotFoundException("Продукт не найден.")
        
        logger.info(
            "Product is successfully deleted",
            extra={"pvz_id": str(pvz_id)}
        )
        
        return {"detail": "Продукт успешно удален"}

        