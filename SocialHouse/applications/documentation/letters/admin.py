from django.contrib import admin

from .models import LetterContract, LetterVisitor, RoomLetter
from ..standardization.admin import DocAdmin


@admin.register(LetterContract)
class LetterContractAdmin(DocAdmin):
    list_display = (
        'serviced_person',
        'date_of_application',
        'reason',
        'contract_type',
        'date_from',
    )
    date_hierarchy = 'date_of_application'
    list_filter = (
        'serviced_person',
        'reason',
        'contract_type',
        'date_of_application',
    )
    search_fields = (
        'serviced_person',
        'date_of_application',
        'reason',
        'contract_type',
    )
    fields = (
        'serviced_person',
        'date_from',
        'date_of_application',
        'reason',
        'contract_type',
    )


@admin.register(LetterVisitor)
class LetterVisitorAdmin(DocAdmin):
    list_display = (
        'visitor',
        'serviced_person',
        'date_of_application',
        'date_from',
        'date_to',
    )
    date_hierarchy = 'date_of_application'
    list_filter = (
        'visitor',
        'serviced_person',
        'date_of_application',
        'date_from',
        'date_to',
    )
    search_fields = (
        'visitor',
        'serviced_person',
        'date_of_application',
        'date_from',
        'date_to',
    )
    fields = (
        'visitor',
        'serviced_person',
        'date_of_application',
        'date_from',
        'date_to',
        'commentary',
    )


@admin.register(RoomLetter)
class RoomLetterAdmin(DocAdmin):
    list_display = (
        'serviced_person',
        'old_place',
        'new_place',
        'date_of_application',
    )
    date_hierarchy = 'date_of_application'
    list_filter = (
        'serviced_person',
        'date_of_application',
        'old_floor',
        'new_floor',
        'old_room',
        'new_room',
    )
    search_fields = (
        'reason',
        'serviced_person',
        'date_of_application',
        'old_floor',
        'new_floor',
        'old_room',
        'new_room',
    )
    fields = (
        'serviced_person',
        'date_of_application',
        'date_from',
        'new_room',
        'new_floor',
        'reason',
    )
