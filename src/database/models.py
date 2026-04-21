from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
import uuid
import datetime


class UserRole(str, Enum):
    MODERATOR = "moderator"
    EMPLOYEE = "employee"


class AllowedCities(str, Enum):
    MOSCOW = "Москва"
    SPB = "Санкт-Петербург"
    KAZAN = "Казань"

class Status(str, Enum):
    IN_PROGRESS = 'in_progress'
    CLOSE = 'close'


class ProductType(str, Enum):
    ELECTRONICS = "электроника"
    CLOTHING = "одежда"
    FOOTWEAR = "обувь"


class Base(DeclarativeBase):
    pass

    
class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.EMPLOYEE)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.UTC), 
        index=True
    )

class PVZ(Base):
    __tablename__ = "pvzs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    city: Mapped[AllowedCities] = mapped_column(nullable=False)
    
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.UTC), 
        index=True
    )


class Reception(Base):
    __tablename__ = "receptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    status: Mapped[Status] = mapped_column(default=Status.IN_PROGRESS)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.UTC), 
        index=True
    )

    products: Mapped[list["Product"]] = relationship(back_populates='reception')

    pvz_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    type: Mapped[ProductType] = mapped_column(nullable=False)

    reception_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('receptions.id'))
    reception: Mapped[Reception] = relationship(back_populates='products')