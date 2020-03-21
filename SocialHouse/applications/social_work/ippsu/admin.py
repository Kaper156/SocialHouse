from django.contrib import admin

from .forms import IncludedServiceForm
from .models import IPPSU, IncludedService


# Register your models here.
@admin.register(IPPSU)
class IPPSUAdmin(admin.ModelAdmin):
    list_display = (
        'social_worker',
        'serviced_person',
        'date_from',
        'date_to',
        'is_archived',
    )
    date_hierarchy = 'date_from'
    list_filter = (
        'social_worker',
        'serviced_person',
        'date_from',
        'date_to',
        'is_archived',
    )


@admin.register(IncludedService)
class IncludedServiceAdmin(admin.ModelAdmin):
    form = IncludedServiceForm
    list_display = ('IPPSU', 'service')
    list_filter = ('IPPSU', 'service')
