from fastapi import APIRouter, Depends
from uuid import UUID

from src.database.models import User
from src.api.dependencies.require_role_dependency import require_roles
from src.database.db import AsyncSession, get_session
from src.services.product_service import ProductService
from src.api.schemas.product_schema import ProductCreate
from src.database.models import UserRole

product_router = APIRouter(
    prefix="/api/product",
    tags=["products"]
)


async def get_product_service(session: AsyncSession = Depends(get_session)):
    return ProductService(session=session)


@product_router.post("/create/pvz/{pvz_id}", status_code=201)
async def create_product(
    pvz_id: UUID,
    product: ProductCreate,
    user: User = Depends(require_roles(UserRole.EMPLOYEE)),
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.create_product(pvz_id=pvz_id, product=product)


@product_router.delete("/create/pvz/{pvz_id}", status_code=200)
async def delete_product(
    pvz_id: UUID,
    user: User = Depends(require_roles(UserRole.EMPLOYEE)),
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.delete_product(pvz_id=pvz_id)
