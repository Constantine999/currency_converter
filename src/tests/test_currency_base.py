from decimal import Decimal

import pytest
from httpx import AsyncClient

from src.exchange_rates import current_base_exchange_rates
from src.schemas import TickersEnum


@pytest.mark.usefixtures("get_current_base_exchange_rate")
class TestCurrentBaseExchangeRates:
    """
    Проверка словаря current_base_exchange_rates из модуля exchange_rates.
    """

    async def test_current_base_exchange_rates_on_equal_lengths_with_tickers(self, ac: AsyncClient):
        """
        Тест на проверку длины словаря current_base_exchange_rates с объектом TickersEnum.
        """
        assert len(current_base_exchange_rates) == len(TickersEnum)

    async def test_current_base_exchange_rates_on_different_lengths_with_tickers(self, ac: AsyncClient):
        """
        Тест на проверку разных длин словаря current_base_exchange_rates с объектом TickersEnum.
        """
        assert len(list(current_base_exchange_rates)[1:]) != len(TickersEnum)

    async def test_current_base_exchange_rates_on_equal_names_with_tickers(self, ac: AsyncClient):
        """
        Тест на полное соответствие имен ключей словаря current_base_exchange_rates
        со значениями объекта TickersEnum.
        """
        tickers_enum = sorted(TickersEnum.__dict__["_member_names_"])
        tickers_current_base_exchange_rates = sorted(current_base_exchange_rates.keys())

        assert tickers_enum == tickers_current_base_exchange_rates

    async def test_current_base_exchange_rates_on_on_different_names_with_tickers(self, ac: AsyncClient):
        """
        Тест на проверку имен ключей словаря current_base_exchange_rates с разными значениями объекта TickersEnum.
        """
        tickers_enum = sorted(TickersEnum.__dict__["_member_names_"] + ["SOS"])
        tickers_current_base_exchange_rates = sorted(current_base_exchange_rates.keys())

        assert tickers_enum != tickers_current_base_exchange_rates

    async def test_current_base_exchange_rates_on_type_value(self, ac: AsyncClient):
        """
        Тест на проверку значения словаря current_base_exchange_rates на тип Decimal.
        """
        result = all(isinstance(value, Decimal) for value in current_base_exchange_rates.values())

        assert result is True

    async def test_current_base_exchange_rates_on_three_symbols_in_key(self, ac: AsyncClient):
        """
        Тест на проверку ключей словаря current_base_exchange_rates на длину в три символа.
        """
        result = all(len(key) == 3 for key in current_base_exchange_rates)

        assert result is True
