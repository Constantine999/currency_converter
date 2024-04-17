from datetime import datetime, timedelta, timezone
from decimal import Decimal

import requests

current_base_exchange_rate: dict = {}
date_base_exchange_rate = datetime(1, 1, 1).date()


async def create_currency_base_with_site_cbr() -> None:
    """
    Формирует таблицу с текущими курсами валют с сайта ЦБР
    """
    global current_base_exchange_rate, date_base_exchange_rate
    current_base_exchange_rate.clear()
    current_base_exchange_rate.update({"RUB": Decimal("1.0000")})

    site_cbr = requests.get(
        "https://www.cbr-xml-daily.ru/daily_json.js",
        json={"key": "value"},
    )

    date = datetime.fromisoformat(site_cbr.json()["Date"]).date()
    timestamp = datetime.fromisoformat(site_cbr.json()["Timestamp"]).date()

    column_with_value = "Value" if timestamp >= date else "Previous"
    for valute in site_cbr.json()["Valute"].values():
        current_base_exchange_rate[valute["CharCode"]] = (
                Decimal(valute[column_with_value]).quantize(Decimal("1.0000")) / valute["Nominal"])

    date_base_exchange_rate = timestamp


async def check_date_currency_base() -> bool:
    """
    Проверка даты получения последней таблицы с сайта ЦБ
    """
    current_date = datetime.now(timezone(timedelta(hours=3))).date()
    if date_base_exchange_rate != current_date:
        await create_currency_base_with_site_cbr()

    return True


async def converter(from_ticker: str, to_ticker: str, value: Decimal) -> Decimal:
    """
    Конвертирует валюту from_ticker со значением value на валюту to_ticker
    """
    result = None
    while result is None:
        try:
            result = (current_base_exchange_rate[from_ticker] * value) / current_base_exchange_rate[to_ticker]
        except IndexError:
            pass

    return result.quantize(Decimal("1.0000"))
