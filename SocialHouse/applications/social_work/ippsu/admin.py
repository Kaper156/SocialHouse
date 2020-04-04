from django.contrib import admin

from .models import IPPSU


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
    search_fields = (
        'social_worker',
        'serviced_person',
    )
