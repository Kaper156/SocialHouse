from django.contrib import admin

from .models import ProvidedJournal, ProvidedService


@admin.register(ProvidedService)
class ProvidedServiceAdmin(admin.ModelAdmin):
    list_display = ('journal', 'date_of', 'service', 'type_of_service')
    list_filter = ('journal', 'date_of', 'service__type_of_service',
                   'journal__ippsu__serviced_person', 'service__service_category')
    # date_hierarchy = 'date_of',
    # filter_horizontal = ('service',)
    # search_fields = ('service__title',)
    autocomplete_fields = ('journal', 'service',)


@admin.register(ProvidedJournal)
class ProvidedServiceJournalAdmin(admin.ModelAdmin):
    list_display = ('ippsu', 'period', 'date_from', 'date_to')
    sortable_by = ('period', 'date_from', 'date_to')
    list_filter = ('ippsu__serviced_person', 'ippsu__executor__worker',
                   'contract_social__serviced_person', 'contract_social__executor__worker',
                   'contract_paid__serviced_person', 'contract_paid__executor__worker',)
    date_hierarchy = 'date_from'
    search_fields = ('ippsu', 'contract_social', 'contract_paid', 'period', 'date_from', 'date_to')
    autocomplete_fields = ('ippsu', 'contract_social', 'contract_paid',)
