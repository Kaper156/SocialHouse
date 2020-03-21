from django.contrib import admin

# Register your models here.
from .models import Statement


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('statement', 'limit')
