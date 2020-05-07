import os

from django.db import models
from django.http import FileResponse
from django.utils import dateformat

from SocialHouse.settings.base import DOCUMENTS_ROOT_FOLDER
from utils.datetime import month_start, month_end


class Document(models.Model):
    class Meta:
        abstract = True

    __template_name__ = ''  # Must be set!
    __template_path__ = ''  # Can be null
    __files_dir__ = 'documents'
    file = models.FilePathField(verbose_name="Файл", editable=False)
    last_modify = models.DateTimeField(verbose_name="Последнее редактирование документа",
                                       editable=False)  # TODO signal pre_save
    content_type = ''

    def __get_other_context_data__(self):
        return {
            'institution': "БУ КЦСОН Тевризского района",
            'kcson_chief': "Берендеева Ольга Валиентиновна",
            'kcson_chief_short': "О.В. Берендеева",
        }

    def get_template_context(self):
        return self.__get_other_context_data__()

    # Once time concatenate folder with templates (relative from current app) and template name
    # -> template_file_path:str
    @classmethod
    def get_template_file_path(cls):
        if cls.__template_path__:
            return cls.__template_path__
        from django.apps import apps
        app_folder = apps.get_app_config(cls._meta.app_label).path
        cls.__template_path__ = os.path.join(app_folder, 'templates', 'documents', cls.__template_name__)
        return cls.__template_path__

    # Get uniq filename -> filename: str
    def get_file_name(self):
        raise NotImplementedError("Template not implemented now")

    # Get relative path (from 'media' to the file) -> file_path: str
    def get_file_path(self):
        return os.path.join(DOCUMENTS_ROOT_FOLDER, self.__files_dir__, self.get_file_name())

    # Run generation of file and writing it to file-field -> file-field
    def generate_file(self):
        raise NotImplementedError("Template not implemented now")

    # Download saved in file-field -> response
    def download(self):
        # response = HttpResponse(content=f.read(), content_type=self.content_type)
        # response['Content-Disposition'] = 'attachment; filename="%s"' % self.get_file_name()
        response = FileResponse(open(self.file, 'rb'), filename=self.get_file_name(), content_type=self.content_type)
        return response


class Journal(models.Model):
    class Meta:
        abstract = True

    date_from = models.DateField(verbose_name="Период от", default=month_start)
    date_to = models.DateField(verbose_name="Период до", default=month_end)

    def period(self):
        return dateformat.format(self.date_from, 'Y-m F')

    period.short_description = "Период"
