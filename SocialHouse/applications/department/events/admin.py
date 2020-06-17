from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date_of',
        'commentary'
    )
    date_hierarchy = 'date_of'
    list_filter = (
        'date_of',
        'department_info',
        'visitors',
    )
    search_fields = (
        'title',
        'date_of',
        'description',
        'commentary',
        'visitors',
    )
    filter_horizontal = (
        'visitors',
    )
    fields = (
        'department_info',
        'title',
        'date_of',
        'description',
        'visitors',
        'commentary',
    )
