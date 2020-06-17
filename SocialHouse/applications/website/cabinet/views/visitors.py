from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from applications.receptionist.visits.models import Visit


@method_decorator(login_required, name='dispatch')
class VisitorsList(ListView):
    template_name = 'cabinet/receptionist/visits/journal.html'
    context_object_name = 'visits'
    paginate_by = 50
    queryset = Visit.objects.order_by('date_of')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context
    #
    # def get_queryset(self):
    #     self.journal = get_object_or_404(ProvidedJournal, id=self.kwargs['provided_journal_id'])
    #     return ProvidedService.objects.filter(journal=self.journal).order_by('date_of')
