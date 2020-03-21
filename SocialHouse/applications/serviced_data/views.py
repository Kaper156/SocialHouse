# Create your views here.
from django.views.generic import DetailView, UpdateView

from applications.serviced_data.models.data import PassportData


class PassportDataDetailView(DetailView):
    model = PassportData
    template_name = 'serviced_data/passport_data_detail.html'
    pk_url_kwarg = 'pk_pas'


class PassportDataUpdateView(UpdateView):
    model = PassportData
    template_name = 'serviced_data/passport_data_update.html'
    pk_url_kwarg = 'pk_pas'
