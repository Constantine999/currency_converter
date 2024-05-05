"""
Настройки фикстур для тестирования с использованием библиотеки pytest
"""

import asyncio
from decimal import Decimal
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from loguru import logger

from src.database import async_engine_test, override_get_db
from src.exchange_rates import get_current_currency_base_with_site_cbr
from src.main import app
from src.models import Base
from src.operations import add_base_current
from src.services import get_time

# Точка переключения в тестовый режим получения объектов AsyncSession для подключения к БД
app.dependency_overrides["TEST_MODE"] = True

test_base_exchange_rates = {}


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def log_test():
    """
    Настройки логирования для тестового режима .
    """

    format = (
        "{extra[utc]} --- "
        "{level}-тестовый режим-  --- "
        "{message}"
    )

    logger.configure(
        handlers=[
            dict(sink="./../logs_test.txt", format=format, level="INFO", rotation="10 Mb", enqueue=True),
        ],
        extra={"common_to_all": "default"},
        patcher=lambda record: record["extra"].update(utc=get_time()),
        activation=[("my_module.secret", False), ("another_library.module", True)],
    )


@pytest.fixture(scope="session", autouse=True)
async def _prepare_database():
    """
    Во время тестов создаем и после всех тестов удаляем таблицу(ы) из БД.
    """

    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session", autouse=True)
async def add_test_base_current():
    """
    Заполняет тестовую таблицу в БД данными по курсам валют.
    """

    global test_base_exchange_rates

    test_base_exchange_rates = get_current_currency_base_with_site_cbr(get_time().date())
    db = await override_get_db().asend(None)

    await add_base_current(
        db=db,
        current_base_exchange_rates=test_base_exchange_rates
    )

    await db.aclose()


@pytest.fixture(scope="function")
async def get_date_base_exchange_rates():
    """
    Возвращает текущую дату курса валют из переменной date_base_exchange_rates .
    """

    from src.exchange_rates import date_base_exchange_rates

    return date_base_exchange_rates


@pytest.fixture(scope="session", autouse=True)
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Генератор запросов для тестового режима.
    """

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def get_test_base_exchange_rates() -> dict[str, Decimal]:
    """
    Для тестового режима вернёт текущий словарь с данными по курсам валют.
    """

    return test_base_exchange_rates
