import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from applications.social_work.providing.models import ProvidedJournal, ProvidedService


@method_decorator(login_required, name='dispatch')
class ProvidedServicesByJournalList(ListView):
    template_name = 'cabinet/social_worker/providing/provided_list.html'
    context_object_name = 'services'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journal'] = get_object_or_404(ProvidedJournal, id=self.kwargs['provided_journal_id'])
        now = datetime.datetime.now().date()
        # now = datetime.datetime(2015, 1, 1).date()
        context['can_manage_journal'] = context['journal'].date_from <= now and context['journal'].date_to >= now
        return context

    def get_queryset(self):
        self.journal = get_object_or_404(ProvidedJournal, id=self.kwargs['provided_journal_id'])
        return ProvidedService.objects.filter(journal=self.journal).order_by('date_of')
