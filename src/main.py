from contextlib import asynccontextmanager
from decimal import Decimal
from typing import Annotated

from fastapi import Depends, FastAPI

from exchange_rates import check_date_currency_base, converter
from schemas import FromAtValueSchema, ResultSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    При каждом запуске приложения формирует таблицу с курсами валют
    """
    await check_date_currency_base()
    yield


app = FastAPI(
    title="Aiti Guru test",
    description="Тестовая работа",
    lifespan=lifespan,
)


@app.get("/api/rates", tags=["CurrencyConvertor", ], response_model=ResultSchema)
async def convert_currency(data: Annotated[FromAtValueSchema, Depends()]) -> ResultSchema:
    """
    **Эндпоинт на конвертирование валют**
    """
    await check_date_currency_base()

    return {
        "result": await converter(
            from_ticker=data.from_ticker,
            to_ticker=data.to_ticker,
            value=data.value,
        )
    }
