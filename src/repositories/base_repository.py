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

    async def create(self, **kwargs):
        new_object = self.model(**kwargs)  
        self.session.add(new_object)
        await self.session.commit()
        await self.session.refresh(new_object)

        return new_object   
        

    
