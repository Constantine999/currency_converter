from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field

tickers: tuple[str, ...] = (
    "RUB", "USD", "EUR", "AUD", "AZN", "AMD", "BYN", "BGN", "BRL", "HUF", "KRW",
    "VND", "HKD", "GEL", "DKK", "AED", "EGP", "INR", "IDR", "KZT", "CAD", "QAR",
    "KGS", "CNY", "MDL", "NZD", "TMT", "NOK", "PLN", "RON", "XDR", "RSD", "SGD",
    "TJS", "THB", "TRY", "UZS", "UAH", "GBP", "CZK", "SEK", "CHF", "ZAR", "JPY",
)


class Ticker(StrEnum):
    """
    Класс с перечислением тикеров валют
    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name


TickersEnum = Ticker("TickersEnum", [*tickers])


class FromAtValueSchema(BaseModel):
    """
    Модель с данными которые получаем на вход
    """
    from_ticker: TickersEnum = Field(default="USD", description="Валюта которую конвертируем")
    to_ticker: TickersEnum = Field(default="RUB", description="Валюта на которую конвертируем")
    value: Decimal = Field(default=1, gt=0, max_digits=24, description="Количество валюты которую конвертируем")


class ResultSchema(BaseModel):
    """
    Модель с данными которые отдаем
    """
    result: float = Field(description="Результат конвертации валюты")
