from fastapi import APIRouter, Depends

from src.database.db import AsyncSession, get_session
from src.database.models import User
from src.api.dependencies.require_role_dependency import require_moderator
from src.services.pvz_service import PVZService
from src.api.schemas.pvz_schema import PVZCreate

pvz_router = APIRouter(
    prefix="/api/pvz",
    tags=["pvz"]
)

async def get_pvz_service(session : AsyncSession = Depends(get_session)):
    return PVZService(session=session)


@pvz_router.post("/new_pvz", status_code=201)
async def create_pvz(
    pvz: PVZCreate,
    user: User = Depends(require_moderator),
    pvz_service: PVZService = Depends(get_pvz_service)
):
    return await pvz_service.create_pvz(data=pvz)