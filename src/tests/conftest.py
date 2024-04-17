from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.exchange_rates import (create_currency_base_with_site_cbr,
                                current_base_exchange_rate)
from src.main import app

client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def get_current_base_exchange_rate():
    await create_currency_base_with_site_cbr()
    yield
