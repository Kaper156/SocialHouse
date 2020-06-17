from django.contrib import admin

from applications.documentation.statistic.models import MeterStatistic


@admin.register(MeterStatistic)
class MeterStatisticAdmin(admin.ModelAdmin):
    list_display = (
        'date_of_formation',
        'date_from',
        'date_to',
        'meter_type',
        # 'meter_data_for_period',
    )
    date_hierarchy = 'date_of_formation'
    list_filter = (
        'date_of_formation',
        'meter_type',
    )
    search_fields = (
        'date_of_formation',
        'meter_type',
    )
    filter_horizontal = ('meter_data_for_period',)
    fields = (
        'date_of_formation',
        'date_from',
        'date_to',
        'meter_type',
        'meter_data_for_period',
    )
