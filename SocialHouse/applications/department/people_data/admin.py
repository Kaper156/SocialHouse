from django.contrib import admin

from .models.serviced_data import PassportData, Privilege, PrivilegeCertificate


@admin.register(PassportData)
class PassportDataAdmin(admin.ModelAdmin):
    list_display = (
        # 'serial',
        # 'number',
        'serviced_person',
        # 'date_of_issue',
        'issued_authority',
    )
    list_filter = ('issued_authority', 'serviced_person',
                   # 'is_dead', 'is_leave',
                   # DeadFilter, LeavedFilter,
                   )


@admin.register(Privilege)
class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ('title',)  # 'sale_guaranteed', 'sale_additional'
    search_fields = ('title',)


@admin.register(PrivilegeCertificate)
class PrivilegeCertificateAdmin(admin.ModelAdmin):
    list_display = ('serviced_person', 'privilege', 'date_of')  # 'sale_guaranteed', 'sale_additional'
    search_fields = ('serviced_person', 'privilege', 'date_of',)
    fields = ('serviced_person', 'privilege', 'date_of')
