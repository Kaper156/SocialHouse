from django.contrib import admin

from applications.documentation.statistic.models import StatisticServices


@admin.register(StatisticServices)
class StatisticServicesAdmin(admin.ModelAdmin):
    list_display = (
        'period_type',
        'date_of_formation',
        'date_from',
        'date_to',
    )
    date_hierarchy = 'date_of_formation'
    list_filter = (
        'period_type',
        'date_of_formation',
        'date_from',
        'date_to',
    )
    search_fields = (
        'period_type',
        'date_of_formation',
        'date_from',
        'date_to',
    )
    fields = (
        'period_type',
        'date_of_formation',
        'acts_social',
        'acts_paid',
    )
