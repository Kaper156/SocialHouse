from django.contrib import admin

# from applications.documentation.reports.models.quarter import QuarterAct, QuarterReportPrivileges
from applications.documentation.reports.admin.abstract import ReportBaseAdmin
from applications.documentation.reports.models.quarter import QuarterReportPrivileges, QuarterAct
from applications.documentation.standardization.admin import DocAdmin


@admin.register(QuarterAct)
class QuarterActAdmin(ReportBaseAdmin):
    filter_horizontal = ('monthly_registries',)
    fields = (
        'date_of_formation',
        'period_from',
        'period_to',

        'service_total',
        'social_passport',
        'monthly_registries',
    )


@admin.register(QuarterReportPrivileges)
class QuarterReportPrivilegesAdmin(DocAdmin):
    filter_horizontal = ('monthly_registries', 'privileges')
    fields = (
        'date_of_formation',
        'period_from',
        'period_to',

        'service_total',
        'social_passport',
        'monthly_registries',
        'privileges'
    )

#
# #
# # @admin.register(QuarterAct)
# # class QuarterActAdmin(DocAdmin):
# #     list_display = (
# #         'date_of_formation',
# #         'service_total',
# #     )
# #     date_hierarchy = 'date_of_formation'
# #     list_filter = (
# #         'date_of_formation',
# #         'service_total',
# #         'monthly_registries'
# #     )
# #     search_fields = (
# #         'date_of_formation',
# #         'service_total',
# #         'monthly_registries'
# #     )
# #
# #     filter_horizontal = (
# #         'monthly_registries',
# #     )
# #     fields = (
# #         'date_of_formation',
# #         'service_total',
# #         'monthly_registries'
# #     )
# #
# @admin.register(QuarterAct)
# class QuarterActAdmin(DocAdmin):
#     list_display = (
#         'date_of_formation',
#         'service_total',
#         'social_passport',
#     )
#     date_hierarchy = 'date_of_formation'
#     list_filter = (
#         'date_of_formation',
#     )
#     search_fields = (
#         'date_of_formation',
#         'service_total',
#         'monthly_registries',
#         'social_passport',
#     )
#
#     filter_horizontal = (
#         'monthly_registries',
#     )
#     fields = (
#         'date_of_formation',
#         'service_total',
#         'social_passport',
#         'monthly_registries',
#     )
#
#
# @admin.register(QuarterReportPrivileges)
# class QuarterReportPrivilegesAdmin(DocAdmin):
#     list_display = (
#         'date_of_formation',
#         'service_total',
#         'social_passport',
#     )
#     date_hierarchy = 'date_of_formation'
#     list_filter = (
#         'date_of_formation',
#     )
#     search_fields = (
#         'date_of_formation',
#         'service_total',
#         'monthly_registries',
#         'social_passport',
#     )
#
#     filter_horizontal = (
#         'monthly_registries',
#         'privileges',
#     )
#     fields = (
#         'date_of_formation',
#         'privileges',
#         'service_total',
#         'social_passport',
#         'monthly_registries',
#     )
