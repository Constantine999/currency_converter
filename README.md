## Задание

### Написать сервис **"Конвертер валют"** который работает по **REST-API**

**_пример запроса:_**

```html
api/rates?from_ticker=USD&to_ticker=RUB&value=1
```

**_пример ответа:_**

```json
{
  "result": 94.0742
}
```

---

### Реализация:

- приложение работает в асинхронном режиме на FastAPI + СУБД PostgreSQL;
- курсы валют получаем c **www.cbr.ru** и сохраняем в таблице БД  **current_base_exchange_rates**;
- ответы на **GET** запросы формируем используя данные из таблицы БД **current_base_exchange_rates**;
- курсы валют забираем c **www.cbr.ru** в двух случаях:
    - при запуске (перезапуске) самого приложения;
    - если дата полученного **GET** запроса отличается от даты сформированой таблицы с курсом валют

### Сруктура приложения:

```

├── src                               # основная директория приложения
│   └── tests                         # директория с тестами pytest
│       ├── __init__.py               # файл инициализатор для пакета tests
│       ├── conftest.py               # основные настройки fixture
│       ├── test_convert_currency.py  # тесты роута /api/rates
│       ├── test_exchange_rates.py    # тесты функций из модуля src/exchange_rates.py
│       ├── test_operations.py        # тесты функций из модуля src/operations.py и таблицы current_base_exchange_rates из БД
│       └── test_services.py          # тесты функций из модуля src/services.py                      
│   ├── __init__.py                   # файл инициализатор для пакета src
│   ├── config.py                     # здесь забираем данные из переменной окружения .env
│   ├── database.py                   # настройки для подключения к БД
│   ├── exchange_rates.py             # здесь находятся все методы работы с валютой
│   ├── log.py                        # модуль настройки логирования для основого режима работы приложения
│   ├── main.py                       # модуль для запуска приложения
│   ├── model.py                      # параметры модели current_base_exchange_rates
│   ├── operations.py                 # модуль для работы с таблицой current_base_exchange_rates
│   ├── schemas.py                    # схемы для валидации значений
│   └── services.py                   # необходимые функции для работы приложения
├── .dockerignore                     # исключаем файлы для docker
├── .env                              # параметры для подключения к БД
├── .gitignore                        # исключаем файлы для git
├── docker-compose.yaml               # инструкция по развертыванию приложения 
├── Dockerfile                        # описание по созданию образа docker
├── pyproject.toml                    # настройки для pytest
├── README.md                         # документация по запуску приложения
├── requirements.txt                  # список зависимостей

```

---
