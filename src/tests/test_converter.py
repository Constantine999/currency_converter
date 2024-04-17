import pytest
from fastapi import status
from httpx import AsyncClient

from src.exchange_rates import converter
from src.schemas import FromAtValueSchema


@pytest.mark.usefixtures("get_current_base_exchange_rate")
class TestConvertCurrency:
    """
    Проверка роута convert_currency
    """

    async def test_convert_currency_on_values_default(self, ac: AsyncClient):
        """
        Тест на проверку значений установленные по умолчанию
        """
        response = await ac.get("/api/rates")
        assert response.status_code == status.HTTP_200_OK

        default_values = [value.default for value in FromAtValueSchema.__dict__['model_fields'].values()]
        assert response.json() == {"result": float(await converter(*default_values))}

    async def test_convert_currency_USD_to_AZN(self, ac: AsyncClient):
        """
        Конвертируем USD в количестве 123456 на AZN
        """
        response = await ac.get("/api/rates", params={"from_ticker": "USD", "to_ticker": "AZN", "value": 123456})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"result": float(await converter("USD", "AZN", 123456))}

    async def test_convert_currency_USD_to_non_existing_ticker(self, ac: AsyncClient):
        """
        Тест если передать несуществующий тикер
        """
        response = await ac.get("/api/rates", params={"from_ticker": "USD", "to_ticker": "SOS", "value": 123456})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_convert_currency_with_negative_value(self, ac: AsyncClient):
        """
        Тест если передать отрицательное значение
        """
        response = await ac.get("/api/rates", params={"from_ticker": "USD", "to_ticker": "JPY", "value": -1})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_convert_currency_with_nil_value(self, ac: AsyncClient):
        """
        Тест если передать нулевое значение
        """
        response = await ac.get("/api/rates", params={"from_ticker": "USD", "to_ticker": "JPY", "value": 0})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_convert_currency_with_value_is_not_digits(self, ac: AsyncClient):
        """
        Тест если передать нулевое значение
        """
        response = await ac.get("/api/rates", params={"from_ticker": "USD", "to_ticker": "JPY", "value": "not_digits"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_convert_currency_with_floating_point_number(self, ac: AsyncClient):
        """
        Тест если передать нулевое значение
        """
        response = await ac.get("/api/rates", params={"from_ticker": "USD", "to_ticker": "JPY", "value": 123.456})
        assert response.status_code == status.HTTP_200_OK
