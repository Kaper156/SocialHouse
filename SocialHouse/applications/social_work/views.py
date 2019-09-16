from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from applications.core.models import Worker
from .models import ServiceJournal
from .forms import ServiceJournalForm


@method_decorator(login_required, name='dispatch')
class ServiceJournalCreateView(CreateView):
    model = Worker
    form_class = ServiceJournalForm
    template_name = 'social_work/services.html'

    def get_context_data(self, **kwargs):
        ctx = super(ServiceJournalCreateView, self).get_context_data(**kwargs)
        worker = Worker.objects.get(user=self.request.user)
        ctx['objs'] = ServiceJournal.objects.filter(employer__worker=worker)
        return ctx
