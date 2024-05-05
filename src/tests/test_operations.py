"""
Тесты функций из модуля src/operations.py
и таблицы current_base_exchange_rates из БД
"""

from decimal import Decimal

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas
from src.database import override_get_db
from src.operations import add_base_current, converter, get_ticker_value


class TestAddBaseCurrent:
    """
    Тесты с функцией add_base_current .
    """

    async def test_add_base_current_send_if_passed_correct_dictionary(
            self,
            get_test_base_exchange_rates: dict[str, Decimal],
    ):
        """
        Тест на проверку передачи словаря с ключами которые должны соответствовать объекту перечисления.

        result: True
        """

        db = await override_get_db().asend(None)

        assert await add_base_current(
            db=db,
            current_base_exchange_rates=get_test_base_exchange_rates,
        ) is True

        await db.aclose()

    async def test_add_base_current_send_if_passed_empty_dictionary(self):
        """
        Тест на проверку передачи пустого словаря.

        result: False
        """

        db = await override_get_db().asend(None)

        assert await add_base_current(
            db=db,
            current_base_exchange_rates={},
        ) is False

        await db.aclose()

    async def test_add_base_current_send_if_passed_not_full_dictionary(self):
        """
        Тест на проверку передачи не полного словаря.

        result: False
        """

        db = await override_get_db().asend(None)

        assert await add_base_current(
            db=db,
            current_base_exchange_rates={'AUD': Decimal('60.1676'), 'AZN': Decimal('54.1255')},
        ) is False

        await db.aclose()


class TestConverter:
    """
    Тесты с функцией converter .
    """

    async def test_converter_with_one_non_existing_ticker(self):
        """
        Тест на передачу одного несуществующего тикера валюты в поле to_ticker .

        result: status.HTTP_404_NOT_FOUND
        """

        db = await override_get_db().asend(None)

        try:
            await converter(db=db,
                            from_ticker="SOS",
                            to_ticker="USD",
                            value=123456,
                            )
        except HTTPException as error:
            assert error.status_code == status.HTTP_404_NOT_FOUND

        await db.aclose()

    async def test_converter_with_two_non_existing_tickers(self):
        """
        Тест на передачу двух несуществующих тикеров валют.

        result: status.HTTP_404_NOT_FOUND
        """

        db = await override_get_db().asend(None)

        try:
            await converter(db=db,
                            from_ticker="SOS",
                            to_ticker="DOS",
                            value=123456,
                            )
        except HTTPException as error:
            assert error.status_code == status.HTTP_404_NOT_FOUND

        await db.aclose()

    async def test_converter_with_value_is_not_digits(self):
        """
        Тест на передачу "строки" в поле для значения.

        result: status.HTTP_404_NOT_FOUND
        """

        db = await override_get_db().asend(None)

        try:
            await converter(db=db,
                            from_ticker="USD",
                            to_ticker="RUB",
                            value="not_digits",
                            )
        except HTTPException as error:
            assert error.status_code == status.HTTP_404_NOT_FOUND

        await db.aclose()

    async def test_converter_with_valid_values(self):
        """
        Тест на передачу существующих тикеров с валидным значением.

        result: True
        """

        db = await override_get_db().asend(None)

        result = await converter(db=db,
                                 from_ticker="USD",
                                 to_ticker="RUB",
                                 value=Decimal(101010),
                                 )

        assert isinstance(result, Decimal) is True

        await db.aclose()

    async def test_converter_with_two_identical_tickers(self):
        """
        Тест на конвертацию с тикеров с валидным значением.

        result: True
        """

        db = await override_get_db().asend(None)

        result = await converter(db=db,
                                 from_ticker="RUB",
                                 to_ticker="RUB",
                                 value=Decimal(202020),
                                 )

        assert isinstance(result, Decimal) is True
        assert result == Decimal(202020)

        await db.aclose()


class TestGetTickerValue:
    """
    Тесты с функцией get_ticker_value .
    """

    async def test_get_ticker_value_send_non_existing_ticker(self):
        """
        Тест на проверку функции get_ticker_value если передать несуществующий в таблице БД тикер.

        result: status.HTTP_404_NOT_FOUND
        """

        db = await override_get_db().asend(None)

        try:
            await get_ticker_value(db=db,
                                   ticker="SOS",
                                   )
        except HTTPException as error:
            assert error.status_code == status.HTTP_404_NOT_FOUND

        await db.aclose()

    async def test_get_ticker_value_send_existing_ticker(self):
        """
        Тест на проверку функции get_ticker_value если передать существующий в таблице БД тикер.

        result: True
        """

        db = await override_get_db().asend(None)
        response = await get_ticker_value(db=db,
                                          ticker="RUB",
                                          )
        await db.aclose()

        assert response == 1


class TestCurrentBaseExchangeRates:
    """
    Тесты таблицы сurrent_base_exchange_rates в БД:
    """

    async def test_current_base_exchange_rates_check_length(self):
        """
        Тест на проверку количества записей в таблице current_base_exchange_rates .

        result: True
        """

        db: AsyncSession = await override_get_db().asend(None)
        result_query = await db.execute(select(func.count(models.CurrentBaseExchangeRates.pk)))
        value = result_query.scalar_one_or_none()
        await db.aclose()

        assert value == len(schemas.TickersEnum)

    async def test_current_base_exchange_rates_checking_for_matching_keys(self):
        """
        Тест на проверку количества идентичности записей
        в таблице current_base_exchange_rates с перечислением schemas.TickersEnum .

        result: True
        """
        db: AsyncSession = await override_get_db().asend(None)
        result = await db.execute(select(models.CurrentBaseExchangeRates.ticker))
        await db.aclose()

        assert sorted(result.scalars().fetchall()) == sorted(schemas.TickersEnum)

    async def test_current_base_exchange_rates_on_on_different_names_with_tickers(self):
        """
        Тест на проверку имен ключей в таблице current_base_exchange_rates с разными значениями объекта TickersEnum.

        result: True
        """

        db: AsyncSession = await override_get_db().asend(None)
        tickers_enum = sorted(schemas.TickersEnum.__dict__["_member_names_"] + ["SOS"])
        result = await db.execute(select(models.CurrentBaseExchangeRates.ticker))
        await db.aclose()

        assert tickers_enum != sorted(result.scalars().fetchall())

    async def test_current_base_exchange_rates_on_type_value(self):
        """
        Тест на проверку значений в таблице current_base_exchange_rates на тип Decimal
        и что значение больше ноля.

        result: True
        """

        db: AsyncSession = await override_get_db().asend(None)
        result = await db.execute(select(models.CurrentBaseExchangeRates.rate))
        await db.aclose()

        assert all(isinstance(value, Decimal) and value > 0 for value in result.scalars().fetchall()) is True

    async def test_current_base_exchange_rates_on_three_symbols_in_key(self):
        """
        Тест на проверку tickers в таблице current_base_exchange_rates на длину в три символа.

        result: True
        """

        db: AsyncSession = await override_get_db().asend(None)
        result = await db.execute(select(models.CurrentBaseExchangeRates.ticker))
        await db.aclose()

        assert all(len(ticker) == 3 for ticker in result.scalars().fetchall()) is True
