from fastapi import APIRouter, Depends

from src.database.db import AsyncSession, get_session
from src.database.models import User, UserRole
from src.api.dependencies.require_role_dependency import require_roles
from src.services.pvz_service import PVZService
from src.api.schemas.pvz_schema import PVZCreate, PVZOut

pvz_router = APIRouter(
    prefix="/api/pvz",
    tags=["pvz"]
)

async def get_pvz_service(session : AsyncSession = Depends(get_session)):
    return PVZService(session=session)


@pvz_router.get("/", status_code=200)
async def get_pvzs(
    user: User = Depends(require_roles(UserRole.MODERATOR)),
    pvz_service: PVZService = Depends(get_pvz_service)
):
    return await pvz_service.get_pvzs()


@pvz_router.post("/create", response_model=PVZOut, status_code=201)
async def create_pvz(
    pvz: PVZCreate,
    user: User = Depends(require_roles(UserRole.MODERATOR)),
    pvz_service: PVZService = Depends(get_pvz_service)
):
    return await pvz_service.create_pvz(data=pvz)