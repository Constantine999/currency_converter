"""
Тесты функций из модуля src/services.py
"""

from datetime import datetime

from fastapi import exceptions, status

from src.services import get_time, http_exception_404, http_exception_422


def test_http_exception_404():
    """
    Тест функции на верный статус код.

    result: status.HTTP_404_NOT_FOUND
    """

    try:
        http_exception_404()
    except exceptions.HTTPException as error:
        assert error.status_code == status.HTTP_404_NOT_FOUND


def test_http_exception_422():
    """
    Тест функции на верный статус код.

    result: status.HTTP_422_UNPROCESSABLE_ENTITY
    """

    try:
        http_exception_422()
    except exceptions.HTTPException as error:
        assert error.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_time_on_correct_result():
    """
    Тест функции на получение корректных данных.

    result: True
    """

    result = get_time()

    assert isinstance(result, datetime) is True
    assert result.tzname() == "UTC+03:00"
