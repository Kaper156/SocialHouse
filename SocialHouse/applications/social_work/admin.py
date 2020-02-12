from django.contrib import admin

from applications.social_work.submodels.ippsu import ProvidedService, IPPSU, IncludedService
from applications.social_work.submodels.services import Service, ServiceMeasurement, ServicesList

# Register your models here.
# TODO https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin

admin.site.register(ProvidedService)  # TODO hidden field type_of_service
admin.site.register(IPPSU)
admin.site.register(IncludedService)

admin.site.register(ServicesList)
admin.site.register(ServiceMeasurement)
admin.site.register(Service)  # Todo add columns (tax, measurement and title)
