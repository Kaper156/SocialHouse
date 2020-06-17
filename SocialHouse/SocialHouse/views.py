from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class DocsView(TemplateView):
    template_name = 'static_pages/docs.html'
