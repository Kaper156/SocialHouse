from django.contrib import admin

from .abstract import ReportBaseAdmin
from ..models.month import RegistryMonthly, DigitalMonthlyReport


@admin.register(RegistryMonthly)
class RegistryMonthlyAdmin(ReportBaseAdmin):
    fields = (
        'date_of_formation',
        'period_from',
        'period_to',

        'service_statistic',
    )


@admin.register(DigitalMonthlyReport)
class DigitalMonthlyReportAdmin(ReportBaseAdmin):
    fields = (
        'date_of_formation',
        'period_from',
        'period_to',

        'service_statistic',
        'social_passport',
        'previous_digital_report',
    )

#
# @admin.register(RegistryMonthly)
# class RegistryMonthlyAdmin(DocAdmin):
#     list_display = (
#         'date_of_formation',
#         'service_total',
#         # TODO: add more fields from ST
#     )
#     date_hierarchy = 'date_of_formation'
#     list_filter = (
#         'date_of_formation',
#         'service_total',
#     )
#     search_fields = (
#         'date_of_formation',
#         'service_total',
#     )
#     fields = (
#         'date_of_formation',
#         'service_total',
#     )
#
#
# @admin.register(DigitalMonthlyReport)
# class DigitalMonthlyReportAdmin(DocAdmin):
#     list_display = (
#         'date_of_formation',
#         'service_total',
#         'social_passport',
#         # TODO: add more fields from ST
#     )
#     date_hierarchy = 'date_of_formation'
#     list_filter = (
#         'date_of_formation',
#         'service_total',
#         'social_passport',
#     )
#     search_fields = (
#         'date_of_formation',
#         'service_total',
#         'social_passport',
#     )
#     fields = (
#         'date_of_formation',
#         'service_total',
#         'social_passport',
#     )
