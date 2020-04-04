from django.contrib import admin

# Register your models here.
from .models import VolumeLimitation, PeriodLimitation


@admin.register(VolumeLimitation)
class VolumeLimitationAdmin(admin.ModelAdmin):
    list_display = ('limit',)


@admin.register(PeriodLimitation)
class PeriodLimitationAdmin(admin.ModelAdmin):
    list_display = ('limit', 'period')
    sortable_by = ('limit', 'period')
