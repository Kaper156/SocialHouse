from applications.documentation.standardization.admin import DocAdmin


class ReportBaseAdmin(DocAdmin):
    list_display = (
        'date_of_formation',
        'period',
    )
    date_hierarchy = 'date_of_formation'
    list_filter = (
        'date_of_formation',
    )
    search_fields = (
        'date_of_formation',
    )
    # fields = (
    #     'date_of_formation',
    #     'service_total',
    # )
