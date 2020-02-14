from django.contrib import admin
from django.contrib.auth.models import User

from .models import Worker, Position, WorkerPosition, ServicedPerson, Privilege, PassportData


class UserAdminInLine(admin.StackedInline):
    model = User
    max_num = 1
    can_delete = False
    verbose_name_plural = "Пользователь"


class WorkerPositionAdminInLine(admin.StackedInline):
    model = WorkerPosition
    max_num = 4
    min_num = 1
    # extra =
    can_delete = True
    verbose_name_plural = "Ставка"


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
        'membership__position'
        # 'date_of_birth' # Todo make abstract filter by age
    )
    search_fields = ('name', 'surname', 'patronymic', 'user__username', 'membership__position__title',)
    # raw_id_fields = (,)
    inlines = (WorkerPositionAdminInLine,)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'purpose', 'group')
    list_filter = ('group',)


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
        # 'date_of_birth' # Todo make abstract filter by age
        'location',
        'privileges',
        'date_of_death',
        'date_of_departure',
    )
    list_filter = (
        'location',
        'date_of_birth',
        'privileges',
        'date_of_death',
        'date_of_departure',
    )
    search_fields = ('name',)


@admin.register(Privilege)
class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ('title', 'sale_guaranteed', 'sale_additional')


@admin.register(PassportData)
class PassportDataAdmin(admin.ModelAdmin):
    list_display = (
        'serial',
        'number',
        'date_of_issue',
        'serviced_person',
    )
    list_filter = ('date_of_issue', 'serviced_person')
