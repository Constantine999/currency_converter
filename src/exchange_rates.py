from datetime import datetime, timedelta, timezone
from decimal import Decimal

import requests

current_base_exchange_rates: dict = {}
date_base_exchange_rates = datetime(1, 1, 1).date()


def create_currency_base_with_site_cbr() -> None:
    """
    Формирует таблицу с текущими курсами валют.
    """
    global current_base_exchange_rates, date_base_exchange_rates
    current_base_exchange_rates.clear()
    current_base_exchange_rates.update({"RUB": Decimal("1.0000")})

    site_cbr = requests.get(
        "https://www.cbr-xml-daily.ru/daily_json.js",
        json={"key": "value"},
    )

    date = datetime.fromisoformat(site_cbr.json()["Date"]).date()
    timestamp = datetime.fromisoformat(site_cbr.json()["Timestamp"]).date()

    column_with_value = "Value" if timestamp >= date else "Previous"
    for valute in site_cbr.json()["Valute"].values():
        current_base_exchange_rates[valute["CharCode"]] = (
                Decimal(valute[column_with_value]).quantize(Decimal("1.0000")) / valute["Nominal"]
        )

    date_base_exchange_rates = timestamp


async def check_date_currency_base() -> bool:
    """
    Проверка даты получения последней таблицы с курсами валют.
    """
    current_date = datetime.now(timezone(timedelta(hours=3))).date()
    if date_base_exchange_rates != current_date:
        create_currency_base_with_site_cbr()

    return True


async def converter(
        from_ticker: str,
        to_ticker: str,
        value: Decimal,
) -> Decimal:
    """
    Конвертирует валюту from_ticker со значением value на валюту to_ticker.
    """

    result = None
    while result is None:
        try:
            result = current_base_exchange_rates[from_ticker] * value / current_base_exchange_rates[to_ticker]
        except IndexError:
            pass

    return result.quantize(Decimal("1.0000"))
