from decimal import Decimal

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from database import async_engine

Base = declarative_base()


class CurrentBaseExchangeRates(Base):
    """
    Таблица с текущим курсом валют .
    """

    __tablename__ = "current_base_exchange_rates"
    __table_args__ = (CheckConstraint('rate > 0'),)

    pk: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)
    rate: Mapped[Decimal] = mapped_column(nullable=False)


async def create_models() -> None:
    """
    Функция для создания таблиц
    """

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_models() -> None:
    """
    Функция для удаления таблицы
    """

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
