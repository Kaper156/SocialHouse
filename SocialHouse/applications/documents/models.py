import os

from django.core.files.storage import FileSystemStorage
from django.db import models
from docxtpl import DocxTemplate

from applications.documents.utils.document import jinja_env

fs = FileSystemStorage(location='/media/docs')


class Document(models.Model):
    class Meta:
        abstract = True

    __template_path__ = ''
    file = models.FileField(verbose_name="Файл", storage=fs, editable=False)

    def get_template_context(self):
        return {
            'kcson_chief': "руководитель БУ КЦСОН Тевризского района Берендеева Ольга Валиентиновна",
        }

    def get_templates_folder_path(self):
        if self.__template_path__:
            return self.__template_path__

        import applications.documents as docs_app
        self.__template_path__ = os.path.join(os.path.dirname(docs_app.__file__), 'templates', 'doc_templates')
        return self.__template_path__

    def get_template(self):
        raise Exception("Template not implemented now")

    def generate_doc(self):
        doc = DocxTemplate(self.get_template())
        context = self.get_template_context()
        doc.render(context, jinja_env=jinja_env)
        doc.save(self.file.path)
        return self.file.path
