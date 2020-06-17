import locale
from datetime import datetime
from decimal import Decimal

import jinja2
import num2words

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

months_ru = {
    1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
    7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь",
}

months_ru_plural = {
    1: "Января", 2: "Февраля", 3: "Марта", 4: "Апреля", 5: "Мая", 6: "Июня",
    7: "Июля", 8: "Августа", 9: "Сентября", 10: "Октября", 11: "Ноября", 12: "Декабря",
}


def month_ru(value: datetime, lower=True):
    if lower:
        return months_ru.get(value.month).lower()
    return months_ru.get(value.month)


def month_plural_ru(value: datetime, lower=True):
    if lower:
        return months_ru_plural.get(value.month).lower()
    return months_ru_plural.get(value.month)


def date_as_numeric(value: datetime):
    return value.strftime("%d.%m.%Y")


def date_with_month_ru(value: datetime):
    return f"{value.day} {month_plural_ru(value)} {value.year}"


def decimal_convert(value: Decimal):
    return locale.currency(value, symbol=False, grouping=True)
    # return str(float(value)).replace('.', ',')


def convert_number_to_words(value):
    return num2words.num2words(value, lang='ru')


def convert_number_to_words_as_currency(value):
    return num2words.num2words(value, lang='ru', to='currency', currency='RUB', separator='')


jinja_env = jinja2.Environment()
jinja_env.filters['month_ru'] = month_ru
jinja_env.filters['month_plural_ru'] = month_plural_ru
jinja_env.filters['dt_num'] = date_as_numeric
jinja_env.filters['dt_month'] = date_with_month_ru

jinja_env.filters['dec'] = decimal_convert
jinja_env.filters['num2words'] = convert_number_to_words
jinja_env.filters['num2wordsAsCurrency'] = convert_number_to_words_as_currency
