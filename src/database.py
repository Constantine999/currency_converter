"""
Модуль с основными и тестовыми настройками подключения к БД.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from config import (DB_HOST, DB_HOST_TEST, DB_NAME, DB_NAME_TEST, DB_PASS,
                    DB_PASS_TEST, DB_PORT, DB_PORT_TEST, DB_USER, DB_USER_TEST)

# Настройки для основного режима работы приложения
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine: AsyncEngine = create_async_engine(
    url=DATABASE_URL,
    future=True,
)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор создания сессий для подключения к БД
    (для основнной работы приложения).
    """

    async with async_session() as session:
        yield session


# Настройки для тестового режима
TEST: bool = False
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

async_engine_test: AsyncEngine = create_async_engine(
    url=DATABASE_URL_TEST,
    poolclass=NullPool,
    future=True,
)

async_session_test = sessionmaker(
    bind=async_engine_test,
    class_=AsyncSession,
    expire_on_commit=False
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор создания сессий для подключения к БД
    (для тестовой работы приложения).
    """

    session = async_session_test()
    try:
        yield session
    finally:
        await session.aclose()
