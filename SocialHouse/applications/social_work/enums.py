from choicesenum import ChoicesEnum


class PeriodEnum(ChoicesEnum):
    DAY = '1', "день"
    WEEK = '7', "неделя"
    MONTH = '31', "месяц"
    UNDEFINED = None, "-Неопределенно-"


class StatementEnum(ChoicesEnum):
    LESS_EQUAL = 'le', "менее/до/не более (включая) (<=)"
    EQUAL = 'eq', "ровно (==)"