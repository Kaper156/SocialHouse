from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from applications.people.models import Worker
# from applications.providing.forms import ProvidedServiceForm
# from applications.providing.models import ProvidedService
# from applications.social_work.utils import get_range_around_month
from applications.social_work.providing.forms import ProvidedServiceForm
from applications.social_work.providing.models import ProvidedService
from utils.datetime import range_month


@method_decorator(login_required, name='dispatch')
class ServiceJournalCreateView(CreateView):
    model = Worker
    form_class = ProvidedServiceForm
    template_name = 'providing/service_journals_list.html'

    def get_context_data(self, **kwargs):
        ctx = super(ServiceJournalCreateView, self).get_context_data(**kwargs)
        worker = Worker.objects.get(user=self.request.user)
        d1, d2 = range_month()
        ctx['objs'] = ProvidedService.objects.filter(employer__worker=worker, date_of__range=(d1, d2))
        ctx['objs_cnt'] = ctx['objs'].count()
        return ctx

    def get_success_url(self):
        return reverse('url_services_journals_create')
