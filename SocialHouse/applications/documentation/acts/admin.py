from django.contrib import admin

from .models.social import SocialAct
from ..standardization.admin import DocAdmin


@admin.register(SocialAct)
class SocialActAdmin(DocAdmin):
    # list_filter = ('living_wage',)
    # filter_horizontal = ('additional_journal',)
    list_display = ('journal', 'period',)
    fields = ('journal', 'additional_journal', 'living_wage', 'avg_per_capita_income')

    # list_filter = ('date_from', 'date_to', 'ippsu__social_worker', 'ippsu__serviced_person')
    # date_hierarchy = 'journal__date_to'
    # search_fields = ('date_from', 'date_to', 'ippsu__social_worker', 'ippsu__serviced_person')
