from django.contrib import admin

from applications.documentation.statistic.models import SocialPassport


@admin.register(SocialPassport)
class SocialPassportAdmin(admin.ModelAdmin):
    list_display = (
        'period_type',
        'date_of_formation',
        'serviced_count',
        'contracts_added',
        'contracts_stopped'
    )
    date_hierarchy = 'date_of_formation'
    list_filter = (
        'period_type',
        'date_of_formation',
        'date_from',
        'date_to',
        'serviced_count',
        'contracts_added',
        'contracts_stopped'
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
    )
