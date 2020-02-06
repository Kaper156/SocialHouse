from django.views.generic import DetailView, ListView
from django.views.generic import TemplateView

from .models import ServicedPerson, PassportData


class IndexView(TemplateView):
    template_name = 'index.html'


class ServicedPersonDetailView(DetailView):
    model = ServicedPerson
    template_name = 'core/serviced_person_detail.html'
    pk_url_kwarg = 'pk_sp'


class ServicedPersonListView(ListView):
    model = ServicedPerson
    template_name = 'core/serviced_person_list.html'
    paginate_by = 50


class PassportDataDetailView(DetailView):
    model = PassportData
    template_name = 'core/passport_data_detail.html'
    pk_url_kwarg = 'pk_pas'
