from django.contrib import admin

# Register your models here.
from applications.documents.admin import DocAdmin
from applications.social_work.acts.models.social import SocialAct


@admin.register(SocialAct)
class SocialActAdmin(DocAdmin):
    # list_filter = ('living_wage',)
    fields = ('journal', 'additional_journal', 'living_wage', 'avg_per_capita_income')
    list_display = ('journal', 'period',)
    # list_filter = ('date_from', 'date_to', 'ippsu__social_worker', 'ippsu__serviced_person')
    # date_hierarchy = 'journal__date_to'
    # search_fields = ('date_from', 'date_to', 'ippsu__social_worker', 'ippsu__serviced_person')
