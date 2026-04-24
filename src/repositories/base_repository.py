from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, data: dict):
        raise NotImplementedError
    
    @abstractmethod
    async def get(self, id: UUID):
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs):
        new_object = self.model(**kwargs)  
        self.session.add(new_object)
        await self.session.commit()
        await self.session.refresh(new_object)

        return new_object

    async def get(self, id: UUID):
        obj = self.session.get(self.model, id)

        return obj


           
    
        

    
