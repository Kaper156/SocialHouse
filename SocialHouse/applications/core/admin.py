from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

from .models import Worker, Position, WorkerPosition, ServicedPerson


class WorkerAdmin(admin.ModelAdmin):
    # TODO filters: FIO, birthday, status
    list_display = ('fullFIO', 'status')


class WorkerAdminInline(admin.StackedInline):
    verbose_name_plural = "Информация о сотруднике"
    model = Worker
    max_num = 1
    can_delete = False


class ExtUserAdminForm(UserAdmin):
    inlines = (WorkerAdminInline,)


class PositionAdminInline(admin.StackedInline):
    verbose_name_plural = "Соответствующая должность"
    model = Position
    max_num = 1
    can_delete = True


class ExtGroupAdminForm(GroupAdmin):
    inlines = (PositionAdminInline,)


admin.site.unregister(User)
admin.site.register(User, ExtUserAdminForm)

admin.site.unregister(Group)
admin.site.register(Group, ExtGroupAdminForm)

admin.site.register(Worker, WorkerAdmin)
admin.site.register(Position)
admin.site.register(WorkerPosition)  # TODO Filter by fio, status, rate
admin.site.register(ServicedPerson)
