from django.urls import path, include

from .views import ProfileView, ProvidedServicesByJournalList


# stub
def knock(*args, **kwargs):
    return ""


# stub
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('sw/provided_journal/<int:provided_journal_id>', ProvidedServicesByJournalList.as_view(),
         name='provided_service_add'),  # TODO
    path('sw/provided_journal/<int:provided_journal_id>', ProvidedServicesByJournalList.as_view(),
         name='provided_services_list'),
    path('rt/', include('applications.receptionist.urls')),
]
