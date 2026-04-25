from fastapi import APIRouter, Depends
from uuid import UUID

from src.services.pvz_reception_service import PVZReceptionService
from src.database.db import AsyncSession, get_session
from src.api.schemas.reception_schema import PVZReceptionCreate
from src.database.models import User, UserRole
from src.api.dependencies.require_role_dependency import require_roles


reception_router = APIRouter(
    prefix="/api/reception",
    tags=["tags"]
)

async def get_reception_service(session: AsyncSession = Depends(get_session)):
    return PVZReceptionService(session=session)
    

@reception_router.post("/create", status_code=201)
async def create_reception(
    reception: PVZReceptionCreate,
    user: User = Depends(require_roles(UserRole.EMPLOYEE)),
    reception_service: PVZReceptionService = Depends(get_reception_service)
):
    return await reception_service.create_reception(reception=reception)
    

@reception_router.put("/close_reception/pvz/{pvz_id}", status_code=201)
async def close_reception(
    pvz_id: UUID,
    user: User = Depends(require_roles(UserRole.EMPLOYEE)),
    reception_service: PVZReceptionService = Depends(get_reception_service)
):
    return await reception_service.close_reception(pvz_id=pvz_id)