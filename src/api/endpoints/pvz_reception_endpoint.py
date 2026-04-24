from fastapi import APIRouter, Depends

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
    

