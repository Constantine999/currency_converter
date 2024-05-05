from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

import log
import schemas
from database import async_session, async_session_test
from exchange_rates import check_date_currency_base
from models import create_models, drop_models
from operations import add_base_current, converter


async def get_session_db():
    """
    Получить сессию для подключения к БД
    """

    if "TEST_MODE" not in app.dependency_overrides:
        async with async_session() as session:
            yield session
    else:
        async with async_session_test() as session:
            yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    При каждом запуске приложения создается таблица в БД с текущим курсом валют.
    """

    if "TEST_MODE" not in app.dependency_overrides:
        logger.info("Приложение CurrencyConverter - начало работы.")

        await create_models()
        logger.info("Таблица в БД - создана")

        await add_base_current(
            db=await get_session_db().asend(None),
            current_base_exchange_rates=await check_date_currency_base(),
        )

    yield

    await drop_models()
    logger.info("Таблица в БД - удалена")
    logger.info("Приложение CurrencyConverter - завершение работы.")


description = """
Приложение **CurrencyConverter** помогает в конвертации валют.

Данные с курсами валют синхронизированы с сайтом [Центрального Банка РФ](http://www.cbr.ru/)

"""

app = FastAPI(
    title="CurrencyConverter",
    description=description,
    lifespan=lifespan,
)


@app.get("/api/rates", tags=["convert currency", ], response_model=schemas.Result, )
async def convert_currency(data: Annotated[schemas.FromToValue, Depends()], db: AsyncSession = Depends(get_session_db)):
    """
    **Роут на конвертирование валют.**
    """

    result = await check_date_currency_base()
    if result is not None:
        await add_base_current(
            db=db,
            current_base_exchange_rates=result,
        )

    return {
        "result": await converter(
            db=db,
            from_ticker=data.from_ticker,
            to_ticker=data.to_ticker,
            value=data.value,
        )
    }
