from contextlib import asynccontextmanager
from decimal import Decimal
from typing import Annotated

from fastapi import Depends, FastAPI

from .exchange_rate import \
    current_base_exchange_rate  # ,check_date_currency_base
from .schemas import FromAtValueSchema, ResultSchema

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """
#     При каждом запуске приложения формируем таблицу с курсом валют
#     """
#     await check_date_currency_base()
#     yield


app = FastAPI(
    title="Aiti Guru test",
    description="Тестовая работа",
    # lifespan=lifespan,
)


async def converter(from_ticker: str, at_ticker: str, value: Decimal) -> Decimal:
    """
    Конвертирует валюту from_ticker со значением value на валюту at_ticker
    """
    result = (current_base_exchange_rate[from_ticker] * value) / current_base_exchange_rate[at_ticker]
    return result.quantize(Decimal("1.0000"))


@app.get("/api/rates", tags=["CurrencyConvertor", ], response_model=ResultSchema)
async def convert_currency(data: Annotated[FromAtValueSchema, Depends()]) -> ResultSchema:
    """
    **Эндпоинт на конвертирование валют**
    """
    # await check_date_currency_base()

    return {
        "result": await converter(
            from_ticker=data.from_ticker,
            at_ticker=data.at_ticker,
            value=data.value,
        )
    }
