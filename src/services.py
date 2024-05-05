"""
Модуль с функциями необходимые для работы приложения
"""

from datetime import datetime, timedelta, timezone
from typing import NoReturn

from fastapi import HTTPException, status


def http_exception_404() -> NoReturn:
    """
    Вызывает исключение со статусом кодом 404.
    """

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Конвертация не была выполнена, отправьте новый запрос.",
    )


def http_exception_422() -> NoReturn:
    """
    Вызывает исключение со статусом кодом 422.
    """

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Было использовано неверное значение.",
    )


def get_time() -> datetime:
    """
    Отправляет текущую дату по московскому времени.
    """

    return datetime.now(timezone(timedelta(hours=3)))
