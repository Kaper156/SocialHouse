from django.contrib import admin

from .models import Worker, Position, WorkerPosition, ServicedPerson

admin.site.register(Worker)
admin.site.register(Position)
admin.site.register(WorkerPosition)
admin.site.register(ServicedPerson)
