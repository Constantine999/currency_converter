from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI

from exchange_rates import check_date_currency_base, converter
from schemas import FromAtValueSchema, ResultSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    При каждом запуске приложения создает словарь с курсом валют.
    """
    await check_date_currency_base()
    yield


description = '''
Приложение **CurrencyConverter** помогает в конвертации валют.

Данные с курсами валют синхронизированы с сайтом [Центрального Банка РФ](http://www.cbr.ru/)

'''

app = FastAPI(
    title="CurrencyConverter",
    description=description,
    lifespan=lifespan,
)


@app.get("/api/rates", tags=["convert currency", ], response_model=ResultSchema)
async def convert_currency(data: Annotated[FromAtValueSchema, Depends()]):
    """
    **Роут на конвертирование валют.**

    """
    await check_date_currency_base()

    return {
        "result": await converter(
            from_ticker=data.from_ticker,
            to_ticker=data.to_ticker,
            value=data.value,
        )
    }
