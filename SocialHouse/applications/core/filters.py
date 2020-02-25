from applications.core.utils.mixin import YearFilter


class DeadFilter(YearFilter):
    parameter_name = 'date_of_death'
    title = "Умершие"
    year_from = 2010


class LeavedFilter(YearFilter):
    parameter_name = 'date_of_departure'
    title = "Покинувшие отделение"
