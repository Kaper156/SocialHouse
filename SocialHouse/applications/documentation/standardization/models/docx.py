from docxtpl import DocxTemplate

from .base import Document
from ..rendering.jinja import jinja_env


class DocumentDocx(Document):
    # class Meta:
    #     abstract = True

    content_type = 'application/msword'
    __files_dir__ = 'docx'

    def get_file_name(self):
        return f'{self._meta.verbose_name}_{self.__str__()}.docx'

    def generate_file(self):
        doc = DocxTemplate(self.get_template_file_path())
        context = self.get_template_context()
        doc.render(context, jinja_env=jinja_env)
        doc.save(self.get_file_path())
        self.file = self.get_file_path()
        return self.file
