from django.contrib import admin
from django.http import FileResponse

from applications.documents.models import SocialAct


class DocAdmin(admin.ModelAdmin):
    change_form_template = 'documents/admin_change_doc.html'

    def response_change(self, request, obj):
        if "_make-docx" in request.POST:
            try:
                file_path = obj.generate_doc()
            except Exception():
                file_path = 'manage.py'
            # with open(file_path, 'rb') as file:
            #     return FileResponse(file)
            return FileResponse(open(file_path, 'rb'))
        return super().response_change(request, obj)


@admin.register(SocialAct)
class SocialActAdmin(DocAdmin):
    # list_filter = ('living_wage',)
    list_display = ('journal', 'period', )
    # list_filter = ('date_from', 'date_to', 'ippsu__social_worker', 'ippsu__serviced_person')
    # date_hierarchy = 'journal__date_to'
    # search_fields = ('date_from', 'date_to', 'ippsu__social_worker', 'ippsu__serviced_person')
