from decimal import Decimal
from random import randint

import pytest
from conftest import get_current_base_exchange_rate
from fastapi import status
from httpx import AsyncClient

from src.exchange_rates import converter, current_base_exchange_rate
from src.schemas import tickers


class TestConvertCurrency:
    async def test_convert_currency_on_values_default(self, ac: AsyncClient):
        """
        Тест результата на значения которое стоят по умолчанию
        """
        response = await ac.get("/api/rates")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"result": 0.0107}

    async def test_convert_currency_USD_to_AZN(self, ac: AsyncClient):
        """
        Конвертируем USD в количестве 123456 на AZN
        """
        response = await ac.get("/api/rates", params={"from_ticker": "USD", "to_ticker": "AZN", "value": 123456})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"result": 209875.2449}

    async def test_convert_currency_USD_to_non_existing_ticker(self, ac: AsyncClient):
        """
        Тест на случай если передать несуществующий тикер
        """
        response = await ac.get("/api/rates", params={"from_ticker": "USD", "to_ticker": "SOS", "value": 123456})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_convert_currency_with_negative_value(self, ac: AsyncClient):
        """
        Тест на случай если передать отрицательное значение
        """
        response = await ac.get("/api/rates", params={"from_ticker": "USD", "to_ticker": "JPY", "value": -1})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_convert_currency_with_nil_value(self, ac: AsyncClient):
        """
        Тест на случай если передать нулевое значение
        """
        response = await ac.get("/api/rates", params={"from_ticker": "USD", "to_ticker": "JPY", "value": 0})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_convert_currency_with_floating_point_number(self, ac: AsyncClient):
        """
        Тест на случай если передать нулевое значение
        """
        response = await ac.get("/api/rates", params={"from_ticker": "USD", "to_ticker": "JPY", "value": 123.456})
        assert response.status_code == status.HTTP_200_OK

    # async def test_converter_each_tickers_with_all(self, ac: AsyncClient):
    #     """
    #     Тест на конвертацию всех тикеров друг с другом
    #     """
    #     for from_ticker in tickers:
    #         for to_ticker in tickers:
    #             if from_ticker != to_ticker:
    #                 value = Decimal(randint(1, 100000))
    #                 response = await ac.get("/api/rates", params={"from_ticker": from_ticker, "to_ticker": to_ticker, "value": value})
    #                 result_convert = await converter(from_ticker, to_ticker, value)
    #                 print(from_ticker, to_ticker, value)
    #                 assert response.status_code == status.HTTP_200_OK
    #                 assert response.json() == {"result": float(result_convert)}
