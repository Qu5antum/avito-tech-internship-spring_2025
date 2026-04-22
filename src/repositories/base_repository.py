from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, data: dict) -> None:
        raise NotImplemented


class BaseRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> None:
        new_object = self.model(**data)  
        self.session.add(new_object)
        await self.session.commit()
        

    
