from django.contrib import admin

from .models import Worker, Position, WorkerPosition, ServicedPerson


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('fullFIO', 'status')


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Position)
admin.site.register(WorkerPosition)
admin.site.register(ServicedPerson)
