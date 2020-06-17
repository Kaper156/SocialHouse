from django.contrib import admin

from .models import DepartmentInfo


@admin.register(DepartmentInfo)
class DepartmentInfoAdmin(admin.ModelAdmin):
    pass
