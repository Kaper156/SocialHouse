from django.contrib import admin

from .models import LivingWage, AveragePerCapitaIncome


@admin.register(LivingWage)
class LivingWageAdmin(admin.ModelAdmin):
    list_display = ('date_to', 'tax',)
    sortable_by = ('date_to', 'tax',)


@admin.register(AveragePerCapitaIncome)
class AveragePerCapitaIncomeAdmin(admin.ModelAdmin):
    list_display = ('serviced_person', 'date_to', 'avg_income')
    sortable_by = ('date_to', 'avg_income', 'serviced_person',)
