from typing import AsyncGenerator
import pytest

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from src.database.db import get_session
from src.main import app


engine = create_async_engine(
    url="sqlite+aiosqlite:///./test.db"
)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session

app.dependency_overrides[get_session] = get_test_session()

