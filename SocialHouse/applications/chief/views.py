from django.views.generic import CreateView

from applications.core.models import ServicedPerson
# Create your views here.
from .forms import ServicedPersonForm


class ServicedPersonCreateView(CreateView):
    model = ServicedPerson
    form_class = ServicedPersonForm
    template_name = 'chief/serviced/serviced_person_create.html'
