from django.contrib import admin

from applications.documentation.reports.admin.abstract import ReportBaseAdmin
from applications.documentation.reports.models.year import DigitalYearReport, CommonYearReport, MeterDataInfo


@admin.register(DigitalYearReport)
class DigitalYearReportAdmin(ReportBaseAdmin):
    fields = (
        'date_of_formation',
        'period_from',
        'period_to',

        'social_passport',
        'service_total',
    )


@admin.register(CommonYearReport)
class CommonYearReportAdmin(ReportBaseAdmin):
    filter_horizontal = ('events',)
    fields = (
        'date_of_formation',
        'period_from',
        'period_to',

        'digital_report',
        'events',
    )


@admin.register(MeterDataInfo)
class MeterDataInfoAdmin(ReportBaseAdmin):
    list_display = (
        'date_of_formation',
        'period',
        'cold_water',
        # 'warm_water',
        # 'gasoline',
        'electricity',
        # 'heating',
    )

    fields = (
        'date_of_formation',
        'period_from',
        'period_to',

        'cold_water',
        'warm_water',
        'gasoline',
        'electricity',
        'heating',
    )
