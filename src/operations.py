"""
Модуль для работы с БД.
"""

from decimal import Decimal
from typing import Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

import models
import schemas
from services import http_exception_404


async def add_base_current(
        db: AsyncSession,
        current_base_exchange_rates: dict[str, Decimal],
) -> None:
    """
    Добавляем данные в БД сurrent_base_exchange_rates .
    """

    if current_base_exchange_rates and sorted(current_base_exchange_rates.keys()) == sorted(schemas.TickersEnum):
        await db.execute(text(f"TRUNCATE TABLE {models.CurrentBaseExchangeRates.__tablename__}"))

        for key, value in current_base_exchange_rates.items():
            db.add(models.CurrentBaseExchangeRates(ticker=key, rate=value))

        await db.commit()
        logger.info(f"Данные в таблице {models.CurrentBaseExchangeRates.__tablename__} - обновлены")

        return True

    else:
        logger.error(f"Ошибка в функции {add_base_current.__name__} "
                     f"- был передан пустой словарь current_base_exchange_rates или тикеры не соответствуют объекту перечисления.")

        return False


async def get_ticker_value(
        db: AsyncSession,
        ticker: str,
) -> Optional[Decimal]:
    """
    Получить значение по ticker из БД.
    """

    value = await db.scalar(
        select(models.CurrentBaseExchangeRates.rate).filter(models.CurrentBaseExchangeRates.ticker == ticker)
    )

    if value is None:
        logger.error(f"Ошибка в функции {get_ticker_value.__name__} - значение из БД не было получено")
        http_exception_404()

    return value


async def converter(
        db: AsyncSession,
        from_ticker: str,
        to_ticker: str,
        value: Decimal,
) -> Decimal:
    """
    Конвертирует валюту from_ticker со значением value на валюту to_ticker .
    """

    if not isinstance(value, Decimal) or value <= 0:
        logger.error(f"Ошибка в функции {converter.__name__} - было передано неверное значение")
        http_exception_404()

    from_ticker_value_rate = await get_ticker_value(db=db, ticker=from_ticker)
    to_ticker_value_rate = await get_ticker_value(db=db, ticker=to_ticker)

    result = from_ticker_value_rate * value / to_ticker_value_rate

    return result.quantize(Decimal("1.0000"))
