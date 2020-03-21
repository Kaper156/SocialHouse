from django.urls import path

import applications.people.views
import applications.serviced_data.views

urlpatterns = [
    path('serviced-person/create', applications.people.views.ServicedPersonCreateView.as_view(),
         name='serviced_person_create'),
    path('serviced-person/<int:pk_sp>', applications.people.views.ServicedPersonDetailView.as_view(),
         name='serviced_person_detail'),
    path('serviced-persons', applications.people.views.ServicedPersonListView.as_view(), name='serviced_person_list'),
    path('serviced-person/<int:pk_sp>/edit', applications.people.views.ServicedPersonUpdateView.as_view(),
         name='serviced_person_update'),
    path('serviced-person/<int:pk_sp>/delete', applications.people.views.ServicedPersonUpdateView.as_view(),
         name='serviced_person_delete'),
]
