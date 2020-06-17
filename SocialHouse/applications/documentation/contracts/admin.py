from django.contrib import admin

from .models import IPPSU, SocialContract, PaidContract
from ..standardization.admin import DocAdmin


class ContractAdminMixin:
    list_display = (
        'executor',
        'serviced_person',
        'date_from',
        'date_expiration',
        'is_archived',
    )
    date_hierarchy = 'date_from'
    list_filter = (
        'executor',
        'serviced_person',
        'date_from',
        'date_expiration',
        'is_archived',
    )
    search_fields = (
        'executor',
        'serviced_person',
    )


@admin.register(SocialContract)
class SocialContractAdmin(ContractAdminMixin, admin.ModelAdmin):
    pass


@admin.register(PaidContract)
class PaidContractAdmin(ContractAdminMixin, admin.ModelAdmin):
    pass


@admin.register(IPPSU)
class IPPSUAdmin(DocAdmin):
    list_display = (
        'executor',
        'serviced_person',
        'date_from',
        'date_expiration',
        'is_archived',
    )
    date_hierarchy = 'date_from'
    list_filter = (
        'executor',
        'serviced_person',
        'date_from',
        'date_expiration',
        'is_archived',
    )
    search_fields = (
        'executor',
        'serviced_person',
    )
    filter_horizontal = ('included_services',)
    fields = (
        'department_info', 'executor', 'serviced_person', 'serial_number', 'date_from', 'is_archived',
        'date_expiration', 'included_services',
    )
