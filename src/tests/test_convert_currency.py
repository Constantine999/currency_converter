"""
Тесты функции convert_currency из модуля src/main.py
"""

import json
from decimal import Decimal
from random import uniform

from fastapi import status
from httpx import AsyncClient


class TestConvertCurrency:
    """
    Тестирование функции convert_currency
    """

    PREFIX: str = "/api/rates"

    async def test_convert_currency_on_values_default(
            self,
            client: AsyncClient,
    ):
        """
        Тест на проверку значений установленные по умолчанию.

        result: status.HTTP_200_OK and True
        """

        response = await client.get(url=self.PREFIX)
        assert response.status_code == status.HTTP_200_OK

        for key, value in json.loads(response._content).items():
            assert key == "result"
            assert isinstance(value, float) is True

    async def test_convert_currency_USD_to_AZN(
            self,
            client: AsyncClient,
    ):
        """
        Тест на конвертацию валюты USD в количестве 123456789 на валюту AZN.

        result: status.HTTP_200_OK
        """

        response = await client.get(
            url=self.PREFIX,
            params={"from_ticker": "USD",
                    "to_ticker": "AZN",
                    "value": 123456789,
                    }
        )
        assert response.status_code == status.HTTP_200_OK
        for key, value in json.loads(response._content).items():
            assert key == "result"
            assert isinstance(value, float) is True

    async def test_convert_currency_USD_to_USD(
            self,
            client: AsyncClient,
    ):
        """
        Тест на конвертацию валюты USD в количестве 123456789 на валюту USD.

        result: status.HTTP_200_OK and True
        """

        response = await client.get(
            url=self.PREFIX,
            params={"from_ticker": "USD",
                    "to_ticker": "USD",
                    "value": 123456789,
                    }
        )
        assert response.status_code == status.HTTP_200_OK

        for key, value in json.loads(response._content).items():
            assert key == "result"
            assert isinstance(value, float) is True
            assert value == 123456789

    async def test_convert_currency_USD_to_non_existing_ticker(
            self,
            client: AsyncClient,
    ):
        """
        Тест на передачу несуществующего тикера валюты в поле to_ticker .

        result: status.HTTP_422_UNPROCESSABLE_ENTITY
        """

        response = await client.get(
            url=self.PREFIX,
            params={"from_ticker": "USD",
                    "to_ticker": "SOS",
                    "value": 123456,
                    }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_convert_currency_with_negative_value(
            self,
            client: AsyncClient,
    ):
        """
        Тест на передачу отрицательного значение в поле для значения.

        result: status.HTTP_422_UNPROCESSABLE_ENTITY
        """

        response = await client.get(
            url=self.PREFIX,
            params={"from_ticker": "USD",
                    "to_ticker": "JPY",
                    "value": -1,
                    }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_convert_currency_with_nil_value(
            self,
            client: AsyncClient,
    ):
        """
        Тест на передачу нулевого значения в поле для значения.

        result: status.HTTP_422_UNPROCESSABLE_ENTITY
        """

        response = await client.get(
            url=self.PREFIX,
            params={"from_ticker": "USD",
                    "to_ticker": "JPY",
                    "value": 0,
                    }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_convert_currency_with_value_is_not_digits(
            self,
            client: AsyncClient,
    ):
        """
        Тест на передачу строки в поле для значения.

        result: status.HTTP_422_UNPROCESSABLE_ENTITY
        """

        response = await client.get(
            url=self.PREFIX,
            params={"from_ticker": "USD",
                    "to_ticker": "JPY",
                    "value": "not_digits",
                    }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_convert_currency_with_floating_point_number(
            self,
            client: AsyncClient,
    ):
        """
        Тест на передачу вещественного значения в поле для значения.

        result: status.HTTP_200_OK
        """

        response = await client.get(
            url=self.PREFIX,
            params={"from_ticker": "USD",
                    "to_ticker": "JPY",
                    "value": 123.456,
                    }
        )

        assert response.status_code == status.HTTP_200_OK

    async def test_convert_currency_all_combinations_tickers_each_other(
            self, client: AsyncClient,
            get_test_base_exchange_rates: dict[str, Decimal],
    ):
        """
        Тест на проверку всех возможных комбинаций тикеров друг с другом с рандомными значениями.

        result: status.HTTP_200_OK
        """

        for from_ticker in get_test_base_exchange_rates:
            for to_ticker in get_test_base_exchange_rates:
                value = Decimal(uniform(1, 10000))
                response = await client.get(
                    url=self.PREFIX,
                    params={"from_ticker": from_ticker,
                            "to_ticker": to_ticker,
                            "value": value.quantize(Decimal("1.0000")),
                            }
                )

                assert response.status_code == status.HTTP_200_OK
