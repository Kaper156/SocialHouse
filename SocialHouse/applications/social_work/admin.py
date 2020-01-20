from django.contrib import admin

# Register your models here.
# TODO https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin

from applications.social_work.submodels.ippsu import ProvidedService
from applications.social_work.submodels.services import Service, ServiceMeasurement

admin.site.register(ProvidedService)  # TODO hidden field type_of_service
admin.site.register(ServiceMeasurement)
admin.site.register(Service)
