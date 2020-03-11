from datetime import datetime

from django.contrib import admin
from django.contrib.auth.models import User

from .filters import DeadFilter, LeavedFilter
from .models import Worker, WorkerPosition, ServicedPerson, Privilege, PassportData, LivingWage, \
    AveragePerCapitaIncome
from .utils.mixin import YearFilter


class UserAdminInLine(admin.StackedInline):
    model = User
    max_num = 1
    can_delete = False
    verbose_name_plural = "Пользователь"


class WorkerPositionAdminInLine(admin.StackedInline):
    model = WorkerPosition
    min_num = 0
    extra = 1
    max_num = 3
    can_delete = True
    verbose_name_plural = "Ставки"


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'FIO',
        'gender',
        'date_of_birth',
        'status',
        'get_positions',
    )
    date_hierarchy = 'date_of_birth'
    list_filter = (
        'status',
        # 'membership__position'
        # 'date_of_birth' # Todo make abstract filter by age
    )
    search_fields = ('name__iexact', 'surname__iexact', 'patronymic__iexact', 'user__username__iexact',
                     'membership__position__title__iexact',)
    # raw_id_fields = (,)
    inlines = (WorkerPositionAdminInLine,)


@admin.register(WorkerPosition)
class WorkerPositionAdmin(admin.ModelAdmin):
    list_display = (
        'worker',
        'position',
        'date_of_appointment',
        'dismissal_date',
        'rate',
    )
    list_filter = (
        'worker',
        'position',
        'date_of_appointment',
        'dismissal_date',
    )


@admin.register(ServicedPerson)
class ServicedPersonAdmin(admin.ModelAdmin):
    list_display = (
        'FIO',
        'gender',
        'date_of_birth',  # Todo make abstract filter by age
        'contract_number',
        'date_of_income',
        'privileges_in_str',
        'location',
    )
    date_hierarchy = 'date_of_birth'
    list_filter = (
        'location',
        'date_of_birth',
        'privileges',
        DeadFilter,
        LeavedFilter,
        # 'date_of_death',
        # 'date_of_departure',
    )
    # raw_id_fields = ('privileges',)
    autocomplete_fields = ('privileges',)
    search_fields = ('name', 'surname', 'patronymic',)


@admin.register(Privilege)
class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ('title',)  # 'sale_guaranteed', 'sale_additional'
    search_fields = ('title',)


@admin.register(PassportData)
class PassportDataAdmin(admin.ModelAdmin):
    list_display = (
        # 'serial',
        # 'number',
        'serviced_person',
        'date_of_issue',
    )
    list_filter = ('date_of_issue', 'serviced_person',
                   # 'is_dead', 'is_leave',
                   # DeadFilter, LeavedFilter,
                   )
    date_hierarchy = 'date_of_issue'


@admin.register(LivingWage)
class LivingWageAdmin(admin.ModelAdmin):
    list_display = ('date_to', 'tax',)
    sortable_by = ('date_to', 'tax',)


@admin.register(AveragePerCapitaIncome)
class AveragePerCapitaIncomeAdmin(admin.ModelAdmin):
    list_display = ('serviced_person', 'date_to', 'avg_income')
    sortable_by = ('date_to', 'avg_income', 'serviced_person',)