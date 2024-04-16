from datetime import datetime, timedelta, timezone
from decimal import Decimal
import requests

current_base_exchange_rate: dict = {}
date_base_exchange_rate = datetime(1, 1, 1).date()


async def create_currency_base_with_site_cbr() -> None:
    """
    Формирует таблицу с текущими курсами валют с сайта ЦБР
    """
    global current_base_exchange_rate, date_base_exchange_rate
    current_base_exchange_rate.clear()
    current_base_exchange_rate.update({"RUB": Decimal("1.0000")})

    site_cbr = requests.get(
        "https://www.cbr-xml-daily.ru/daily_json.js",
        json={"key": "value"},
    )

    date = datetime.fromisoformat(site_cbr.json()["Date"]).date()
    timestamp = datetime.fromisoformat(site_cbr.json()["Timestamp"]).date()

    column_with_value = "Value" if timestamp >= date else "Previous"
    for valute in site_cbr.json()["Valute"].values():
        current_base_exchange_rate[valute["CharCode"]] = (
                Decimal(valute[column_with_value]).quantize(Decimal("1.0000")) / valute["Nominal"])

    date_base_exchange_rate = timestamp


async def check_date_currency_base() -> bool:
    """
    Проверка даты получения последней таблицы с сайта ЦБ
    """
    current_date = datetime.now(timezone(timedelta(hours=3))).date()
    if date_base_exchange_rate != current_date:
        await create_currency_base_with_site_cbr()

    return True

# Данные для отладки
# current_base_exchange_rate.update(
#     {'RUB': Decimal('1.0000'), 'AUD': Decimal('60.7206'), 'AZN': Decimal('55.0524'), 'GBP': Decimal('116.3780'), 'AMD': Decimal('0.236479'),
#      'BYN': Decimal('28.6529'), 'BGN': Decimal('50.9711'), 'BRL': Decimal('18.2218'), 'HUF': Decimal('0.253732'),
#      'VND': Decimal('0.00388401'), 'HKD': Decimal('11.9771'), 'GEL': Decimal('35.0403'), 'DKK': Decimal('13.3628'),
#      'AED': Decimal('25.4838'), 'USD': Decimal('93.5891'), 'EUR': Decimal('99.7934'), 'EGP': Decimal('1.93527'), 'INR': Decimal('1.1216'),
#      'IDR': Decimal('0.00588352'), 'KZT': Decimal('0.208956'), 'CAD': Decimal('67.9857'), 'QAR': Decimal('25.7113'),
#      'KGS': Decimal('1.05015'), 'CNY': Decimal('12.8844'), 'MDL': Decimal('5.2868'), 'NZD': Decimal('55.6106'), 'NOK': Decimal('8.60368'),
#      'PLN': Decimal('23.2757'), 'RON': Decimal('20.0560'), 'XDR': Decimal('123.1661'), 'SGD': Decimal('68.7953'), 'TJS': Decimal('8.56659'),
#      'THB': Decimal('2.55485'), 'TRY': Decimal('2.92148'), 'TMT': Decimal('26.7397'), 'UZS': Decimal('0.00738842'),
#      'UAH': Decimal('2.37542'), 'CZK': Decimal('3.93761'), 'SEK': Decimal('8.61642'), 'CHF': Decimal('102.5297'),
#      'RSD': Decimal('0.851302'), 'ZAR': Decimal('5.00835'), 'KRW': Decimal('0.0676222'), 'JPY': Decimal('0.610138'), }
# )
