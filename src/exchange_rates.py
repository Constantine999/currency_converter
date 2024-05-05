"""
Модуль по парсингу курса валют с сайта ЦБР.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

import requests
from bs4 import BeautifulSoup
from fastapi import status
from loguru import logger

from services import get_time, http_exception_404

# Дата последнего успешного запроса на сайт www.cbr.ru
date_base_exchange_rates = datetime(1, 1, 1).date()


async def check_date_currency_base() -> Optional[dict[str, Decimal]]:
    """
    Проверяет дату получения последней таблицы с курсом валют.
    """

    current_date = get_time().date()
    if date_base_exchange_rates != current_date:
        return get_current_currency_base_with_site_cbr(current_date)


def get_soup_site_cbr(date_query: datetime) -> BeautifulSoup:
    """
    Генерирует объект soup страницы с курсом валют.
    """

    site_cbr = requests.get(f"https://www.cbr.ru/currency_base/daily/?To={date_query.strftime("%d.%m.%Y")}")
    if site_cbr.status_code == status.HTTP_200_OK:
        logger.info(f"В функции {get_soup_site_cbr.__name__} - сделал GET запрос на сайт ЦБР")
        return BeautifulSoup(site_cbr.text, "html.parser")

    logger.error(f"Ошибка в функции {get_soup_site_cbr.__name__} - в отправлении запроса на сайт www.cbr.ru")
    http_exception_404()


def get_current_currency_base_with_site_cbr(date_query: datetime) -> Optional[dict[str, Decimal]]:
    """
    Получить текущий курс валют с сайта ЦБР.
    """

    global date_base_exchange_rates
    # Создаем словарь для курса валют
    current_base_exchange_rates = {}

    # Парсим основную страницу по курсам
    soup_site_cbr = get_soup_site_cbr(date_query)

    # Добавляем в словарь данные
    try:
        for line in soup_site_cbr.find("div", class_="table-wrapper").find_all("tr")[1:]:
            _, ticker, nominal_value, _, current_course = line.text.strip().split("\n")

            current_course = Decimal(current_course.replace(",", ".")).quantize(Decimal("1.0000"))
            current_base_exchange_rates[ticker] = current_course / int(nominal_value)

    except AttributeError as error:
        logger.error(
            f"Ошибка {error=} в функции {get_current_currency_base_with_site_cbr.__name__} "
            f"- в поиске таблице курса валют на сайте www.cbr.ru"
        )
        http_exception_404()

    date_base_exchange_rates = date_query
    current_base_exchange_rates.update({"RUB": Decimal("1.0000")})

    return current_base_exchange_rates
