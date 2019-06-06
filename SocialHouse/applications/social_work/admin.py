from django.contrib import admin

# Register your models here.
# TODO https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin

from .models import ServiceJournal, Period, Service, ServiceTariff

admin.site.register(ServiceJournal)
admin.site.register(Period)
admin.site.register(Service)
admin.site.register(ServiceTariff)
