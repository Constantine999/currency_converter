from datetime import datetime, timedelta, timezone
from decimal import Decimal

import requests

current_base_exchange_rate: dict = {}
date_base_exchange_rate = datetime(1, 1, 1).date()


# async def create_currency_base_with_site_cbr() -> None:
#     """
#     Сформировать таблицу с текущими курсами валют с сайта ЦБР
#     """
#     global current_base_exchange_rate, date_base_exchange_rate
#     current_base_exchange_rate.clear()
#     current_base_exchange_rate.update({"RUB": Decimal("1.0000")})
#
#     site_cbr = requests.get(
#         "https://www.cbr-xml-daily.ru/daily_json.js",
#         json={"key": "value"},
#     )
#
#     for valute in site_cbr.json()["Valute"].values():
#         current_base_exchange_rate[valute["CharCode"]] = (
#                 Decimal(valute["Value"]).quantize(Decimal("1.0000")) / valute["Nominal"])
#
#     date_base_exchange_rate = datetime.fromisoformat(site_cbr.json()["Timestamp"]).date()


# async def check_date_currency_base() -> bool:
#     """
#     Проверка даты получения последней таблицы с сайта ЦБ
#     """
#     current_date = datetime.now(timezone(timedelta(hours=3))).date()
#     if date_base_exchange_rate != current_date:
#         await create_currency_base_with_site_cbr()
#
#     return True

# Данные для отладки
current_base_exchange_rate.update(
    {'RUB': Decimal('1.0000'), 'AUD': Decimal('60.9802'), 'AZN': Decimal('54.9658'), 'GBP': Decimal('116.9893'),
     'AMD': Decimal('0.237259'), 'BYN': Decimal('28.6280'), 'BGN': Decimal('51.2589'), 'BRL': Decimal('18.4078'),
     'HUF': Decimal('0.25452'), 'VND': Decimal('0.00388016'), 'HKD': Decimal('11.9445'), 'GEL': Decimal('34.9708'),
     'DKK': Decimal('13.4381'), 'AED': Decimal('25.4437'), 'USD': Decimal('93.4419'), 'EUR': Decimal('99.7264'),
     'EGP': Decimal('1.96343'), 'INR': Decimal('1.1205'), 'IDR': Decimal('0.00587426'), 'KZT': Decimal('0.208385'),
     'CAD': Decimal('68.2456'), 'QAR': Decimal('25.6709'), 'KGS': Decimal('1.0485'), 'CNY': Decimal('12.8685'),
     'MDL': Decimal('5.29623'), 'NZD': Decimal('56.1539'), 'NOK': Decimal('8.62918'), 'PLN': Decimal('23.3704'),
     'RON': Decimal('20.0326'), 'XDR': Decimal('123.3461'), 'SGD': Decimal('68.9405'), 'TJS': Decimal('8.54412'),
     'THB': Decimal('2.55083'), 'TRY': Decimal('2.91689'), 'TMT': Decimal('26.6977'), 'UZS': Decimal('0.00737163'),
     'UAH': Decimal('2.38569'), 'CZK': Decimal('3.9291'), 'SEK': Decimal('8.69428'), 'CHF': Decimal('102.3796'),
     'RSD': Decimal('0.854819'), 'ZAR': Decimal('5.00048'), 'KRW': Decimal('0.067938'), 'JPY': Decimal('0.610691')}
)
