# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView

from applications.people.forms import ServicedPersonForm
from applications.people.models.people import ServicedPerson
from applications.serviced_data.forms import PassportDataForm
from utils.mixin import OneToOneCreateView


class ServicedPersonCreateView(OneToOneCreateView):
    # Add serviced person and related passport-data
    template_name = 'people/serviced_person_create.html'
    main_form = ServicedPersonForm
    sub_form = PassportDataForm
    sub_relation_field = 'serviced_person'
    success_url = reverse_lazy('serviced_person_list')


class ServicedPersonDetailView(DetailView):
    model = ServicedPerson
    template_name = 'people/serviced_person_detail.html'
    pk_url_kwarg = 'pk_sp'


class ServicedPersonListView(ListView):
    model = ServicedPerson
    template_name = 'people/serviced_person_list.html'
    paginate_by = 50


class ServicedPersonUpdateView(UpdateView):
    model = ServicedPerson
    template_name = 'people/serviced_person_update.html'
    pk_url_kwarg = 'pk_sp'


class ServicedPersonDeleteView(DeleteView):
    model = ServicedPerson
    template_name = 'people/serviced_person_delete.html'
    pk_url_kwarg = 'pk_sp'
