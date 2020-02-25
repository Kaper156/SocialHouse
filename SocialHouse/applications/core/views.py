from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, UpdateView
from django.views.generic import TemplateView

from .forms import ServicedPersonForm, PassportDataForm
from .models import ServicedPerson, PassportData
from .utils.mixin import OneToOneCreateView


class IndexView(TemplateView):
    template_name = 'index.html'


class ServicedPersonCreateView(OneToOneCreateView):
    # Add serviced person and related passport-data
    template_name = 'core/serviced_person_create.html'
    main_form = ServicedPersonForm
    sub_form = PassportDataForm
    sub_relation_field = 'serviced_person'
    success_url = reverse_lazy('serviced_person_list')


class ServicedPersonDetailView(DetailView):
    model = ServicedPerson
    template_name = 'core/serviced_person_detail.html'
    pk_url_kwarg = 'pk_sp'


class ServicedPersonListView(ListView):
    model = ServicedPerson
    template_name = 'core/serviced_person_list.html'
    paginate_by = 50


class ServicedPersonUpdateView(UpdateView):
    model = ServicedPerson
    template_name = 'core/serviced_person_update.html'
    pk_url_kwarg = 'pk_sp'


class ServicedPersonDeleteView(DeleteView):
    model = ServicedPerson
    template_name = 'core/serviced_person_delete.html'
    pk_url_kwarg = 'pk_sp'


class PassportDataDetailView(DetailView):
    model = PassportData
    template_name = 'core/passport_data_detail.html'
    pk_url_kwarg = 'pk_pas'


class PassportDataUpdateView(UpdateView):
    model = PassportData
    template_name = 'core/passport_data_update.html'
    pk_url_kwarg = 'pk_pas'
