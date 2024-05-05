"""
Модуль настройки логирования для основого режима работы приложения
"""

from loguru import logger

from services import get_time

format = (
    "{extra[utc]} --- "
    "{level} --- "
    "{message}"
)

logger.configure(
    handlers=[
        dict(sink="./../logs.txt", format=format, level="INFO", rotation="10 Mb", enqueue=True),
    ],
    extra={"common_to_all": "default"},
    patcher=lambda record: record["extra"].update(utc=get_time()),
    activation=[("my_module.secret", False), ("another_library.module", True)],
)
