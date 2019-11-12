from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from applications.core.models import Worker
from .forms import ServiceJournalForm
from .models import ServiceJournal
from .utils import get_range_around_month


@method_decorator(login_required, name='dispatch')
class ServiceJournalCreateView(CreateView):
    model = Worker
    form_class = ServiceJournalForm
    template_name = 'social_work/services.html'

    def get_context_data(self, **kwargs):
        ctx = super(ServiceJournalCreateView, self).get_context_data(**kwargs)
        worker = Worker.objects.get(user=self.request.user)
        d1, d2 = get_range_around_month()
        ctx['objs'] = ServiceJournal.objects.filter(employer__worker=worker, date_of__range=(d1, d2))
        ctx['objs_cnt'] = ctx['objs'].count()
        return ctx

    def get_success_url(self):
        return reverse('url_services_journals_create')
