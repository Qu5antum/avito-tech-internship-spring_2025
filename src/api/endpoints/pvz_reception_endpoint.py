from fastapi import APIRouter, Depends
from uuid import UUID
from datetime import datetime

from src.services.pvz_reception_service import PVZReceptionService
from src.database.db import AsyncSession, get_session
from src.api.schemas.reception_schema import PVZReceptionCreate, PVZReceptionOut
from src.database.models import User, UserRole
from src.api.dependencies.require_role_dependency import require_roles


reception_router = APIRouter(
    prefix="/api/reception",
    tags=["tags"]
)

async def get_reception_service(session: AsyncSession = Depends(get_session)):
    return PVZReceptionService(session=session)
    

@reception_router.post("/create", response_model=PVZReceptionOut, status_code=201)
async def create_reception(
    reception: PVZReceptionCreate,
    user: User = Depends(require_roles(UserRole.EMPLOYEE)),
    reception_service: PVZReceptionService = Depends(get_reception_service)
):
    return await reception_service.create_reception(reception=reception)
    

@reception_router.put("/close_reception/pvz/{pvz_id}", response_model=PVZReceptionOut, status_code=200)
async def close_reception(
    pvz_id: UUID,
    user: User = Depends(require_roles(UserRole.EMPLOYEE)),
    reception_service: PVZReceptionService = Depends(get_reception_service)
):
    return await reception_service.close_reception(pvz_id=pvz_id)


@reception_router.get("/pvz/{pvz_id}/detail", status_code=200)
async def get_reception_detail(
    pvz_id: UUID,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    user: User = Depends(require_roles(UserRole.MODERATOR)),
    reception_service: PVZReceptionService = Depends(get_reception_service)
):
    return await reception_service.reception_detail(pvz_id=pvz_id, from_date=from_date, to_date=to_date)
