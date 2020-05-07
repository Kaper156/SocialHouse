from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


# всем привет, делаю обертку для скачивания файлов в админке. Сделал поле со ссылкой на файл (спрашивал вчера), можно ли
class DocAdmin(admin.ModelAdmin):
    '''
    Inherits behavior for downloading inner files and show link, date-of-update
    '''

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # Fields which inherited by all Document-models
        downloading_fields = ['document_link', 'last_modify']
        # Add them as read-only
        self.readonly_fields = tuple(list(self.readonly_fields) + downloading_fields)
        # Form url-name to downloading by using meta of class
        self.download_document_url_name = f'{self.model._meta.app_label}_{self.model._meta.model_name}_download-file'
        # Wrap fields and downloading_fields to fieldsets
        self.fieldsets = (
            ('Данные', {
                'fields': tuple(self.fields or [])
            }),
            ('Файл документа', {
                'fields': tuple(downloading_fields),
            }),
        )
        self.fields = None
        # TODO make form-set

    # TODO add as second button "Save and download"
    # def response_change(self, request, obj):
    #     if "_make-docx" in request.POST:
    #         try:
    #             file_path = obj.generate_doc()
    #         except Exception():
    #             file_path = 'manage.py'
    #         # with open(file_path, 'rb') as file:
    #         #     return FileResponse(file)
    #         return FileResponse(open(file_path, 'rb'))
    #     return super().response_change(request, obj)

    def get_urls(self):
        # Add url for downloading document
        urls = super(DocAdmin, self).get_urls()
        urls += [
            url(r'^download-file/(?P<pk>\d+)$', self.download_document, name=self.download_document_url_name),
        ]
        return urls

    def document_link(self, obj):
        # Represent html-link for download document
        if obj.file:
            return format_html(
                '<a href="{}" class="button">Скачать документ</a>',
                reverse(f'admin:{self.download_document_url_name}', args=[obj.pk])
            )
        return "Документ ещё не был сформирован, сохраните его, чтобы скачать"

    def download_document(self, req, pk):
        # Call obj.download by PK (id)
        obj = self.model.objects.get(id=pk)
        return obj.download()

    document_link.short_description = "Документ"
