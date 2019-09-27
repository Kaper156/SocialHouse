from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from applications.core.models import Worker
from .models import ServiceJournal
from .forms import ServiceJournalForm
from .utils import get_range_around_month
from django.db.models import Q


@method_decorator(login_required, name='dispatch')
class ServiceJournalCreateView(CreateView):
    model = Worker
    form_class = ServiceJournalForm
    template_name = 'social_work/services.html'

    def get_context_data(self, **kwargs):
        ctx = super(ServiceJournalCreateView, self).get_context_data(**kwargs)
        worker = Worker.objects.get(user=self.request.user)
        d1, d2 = get_range_around_month()
        # TODO fix multiply of SJ
        ctx['objs'] = ServiceJournal.objects.filter(Q(employer__worker=worker)
                                                    & Q(service__servicejournal__date_of__range=(d1, d2)))
        ctx['objs_cnt'] = ctx['objs'].count()
        return ctx
