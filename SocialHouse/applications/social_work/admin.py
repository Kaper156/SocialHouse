from django.contrib import admin

# Register your models here.
# TODO https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin

from .models import ServiceJournal, ServiceMeasurement, Service

admin.site.register(ServiceJournal)  # TODO hidden field type_of_service
admin.site.register(ServiceMeasurement)
admin.site.register(Service)
