"""
Тесты функций из модуля src/exchange_rates.py
"""

from datetime import datetime, timedelta
from decimal import Decimal

from bs4 import BeautifulSoup
from fastapi import status

from src.exchange_rates import (get_current_currency_base_with_site_cbr,
                                get_soup_site_cbr, )
from src.services import get_time


class TestDateBaseExchangeRates:
    """
    Тесты переменной date_base_exchange_rates .
    """

    async def test_date_base_exchange_rates(
            self,
            get_date_base_exchange_rates: datetime,
    ):
        """
        Тест на проверку текущей даты в переменной date_base_exchange_rates .

        result: True
        """

        assert get_date_base_exchange_rates == get_time().date()


class TestGetCurrentCurrencyBaseWithSiteCbr:
    """
    Тесты функции get_current_currency_base_with_site_cbr .
    """

    async def test_get_current_currency_base_with_site_cbr_for_return_valid_data(self):
        """
        Тест на проверку:
        - на возврат объекта dict;
        - все ключи являются типом str в верхнем регистре;
        - у всех ключей значения Decimal;

        result: True
        """

        result: dict[str, Decimal] = get_current_currency_base_with_site_cbr(get_time().date())

        assert isinstance(result, dict) is True
        assert all(ticker.isupper() for ticker in result) is True
        assert all(isinstance(ticker, Decimal) for ticker in result.values()) is True

    async def test_get_current_currency_base_with_site_cbr_for_return_valid_data_but_plus_two_days_from_current_date(self):
        """
        Тест на проверку, если к передаваемой дате на момент теста добавить + 2 дня

        result: True
        """

        result_current_date_plus_two_days = get_current_currency_base_with_site_cbr((get_time() + timedelta(days=2)).date())
        result_current_date = get_current_currency_base_with_site_cbr(get_time().date())

        assert result_current_date_plus_two_days == result_current_date

    async def test_get_current_currency_base_with_site_cbr_on_raise_404_error(self):
        """
        Тест на передачу неверной даты.

        result: status.HTTP_404_NOT_FOUND
        """

        try:
            get_current_currency_base_with_site_cbr(datetime(1900, 1, 1).date())
        except status.HTTP_404_NOT_FOUND as error:
            assert error.status_code == status.HTTP_404_NOT_FOUND


class TestGetSoupCBR:
    """
    Тесты функции get_soup_site_cbr .
    """

    async def test_get_soup_site_cbr_receive_successful_result(self):
        """
        Тест на получение успешного результата

        result: True
        """

        result: BeautifulSoup = get_soup_site_cbr(get_time().date())
        assert isinstance(result, BeautifulSoup) is True

    async def test_get_soup_site_cbr_on_raise_attribute_error(self):
        """
        Тест на передачу другого вместо даты другого значения .

        result: "AttributeError"
        """

        try:
            get_soup_site_cbr("no date")
        except AttributeError as error:
            assert error.__class__.__name__ == "AttributeError"

    async def test_get_soup_site_cbr_on_raise_404_error(self):
        """
        Тест на передачу неверной даты

        result: status.HTTP_404_NOT_FOUND
        """

        try:
            get_soup_site_cbr(datetime(1, 1, 1).date())
        except status.HTTP_404_NOT_FOUND as error:
            assert error.status_code == status.HTTP_404_NOT_FOUND
