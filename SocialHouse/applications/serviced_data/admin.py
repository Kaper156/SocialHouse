from django.contrib import admin

from applications.serviced_data.models import LivingWage, AveragePerCapitaIncome
# Register your models here.
from applications.serviced_data.models import Privilege, PassportData


@admin.register(Privilege)
class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ('title',)  # 'sale_guaranteed', 'sale_additional'
    search_fields = ('title',)


@admin.register(PassportData)
class PassportDataAdmin(admin.ModelAdmin):
    list_display = (
        # 'serial',
        # 'number',
        'serviced_person',
        'date_of_issue',
    )
    list_filter = ('date_of_issue', 'serviced_person',
                   # 'is_dead', 'is_leave',
                   # DeadFilter, LeavedFilter,
                   )
    date_hierarchy = 'date_of_issue'


@admin.register(LivingWage)
class LivingWageAdmin(admin.ModelAdmin):
    list_display = ('date_to', 'tax',)
    sortable_by = ('date_to', 'tax',)


@admin.register(AveragePerCapitaIncome)
class AveragePerCapitaIncomeAdmin(admin.ModelAdmin):
    list_display = ('serviced_person', 'date_to', 'avg_income')
    sortable_by = ('date_to', 'avg_income', 'serviced_person',)
