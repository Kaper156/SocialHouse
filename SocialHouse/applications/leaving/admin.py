from django.contrib import admin

from .models import Travel, SickLeave


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = (
        'serviced_person',
        'date_from',
        'date_to',
        'commentary',
        'visitor',
    )
    sortable_by = ('serviced_person', 'date_from', 'date_to',)
    list_filter = ('serviced_person', 'visitor')
    search_fields = ('serviced_person__name',
                     'serviced_person__surname',
                     'serviced_person__patronymic',
                     'visitor__name',
                     'visitor__surname',
                     'visitor__patronymic',)
    autocomplete_fields = ('serviced_person', 'serviced_person', 'serviced_person')


@admin.register(SickLeave)
class SickLeaveAdmin(admin.ModelAdmin):
    list_display = (
        'serviced_person',
        'date_from',
        'date_to',
        'commentary',
        'diagnose',
    )
    list_filter = ('serviced_person', 'date_from', 'date_to')
    search_fields = ('serviced_person__name',
                     'serviced_person__surname',
                     'serviced_person__patronymic',)
    autocomplete_fields = ('serviced_person', 'serviced_person', 'serviced_person')
