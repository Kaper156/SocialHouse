from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    def get_context_data(self, **kwargs):
        ctx = super(ProfileView, self).get_context_data(**kwargs)

        # from applications.department.people.models import WorkerPosition
        # WorkerPosition.objects.all().filter(dismissal_date__isnull=False, date_of_appointment__lte=)
        # now = datetime.datetime.now()
        # ctx['memberships'] = self.request.user.worker.membership.all().active()
        # for wp in ctx['memberships'].social_workers():
        #     # " ".join(map(str, IPPSUs.all()))
        #     IPPSUs = IPPSU.objects.filter(executor=wp, is_archived=False,
        #                                   date_expiration__gte=now.date(), date_from__lt=now.date())
        #     wp.serviced_peoples = list(ippsu.serviced_person for ippsu in IPPSUs)
        #     print(wp.__dict__)
        # # if ctx['memberships'].count() > 0:
        # # print(f"{ctx['memberships']}")

        # ctx['ippsus'] = self.request.user.worker.membership.first().get_active_IPPSU_set()
        # print(ctx['ippsus'])
        return ctx

    template_name = 'cabinet/profile.html'
