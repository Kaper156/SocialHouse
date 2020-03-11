from datetime import datetime

import jinja2

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


def datetime_as_numeric(value: datetime):
    return value.strftime("%d.%m.%Y")


jinja_env = jinja2.Environment()
jinja_env.filters['month_ru'] = month_ru
jinja_env.filters['month_plural_ru'] = month_plural_ru
jinja_env.filters['dt_num'] = datetime_as_numeric
