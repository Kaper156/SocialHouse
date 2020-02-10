from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('serviced-person/create', views.ServicedPersonCreateView.as_view(), name='serviced_person_create'),
    path('serviced-person/<int:pk_sp>', views.ServicedPersonDetailView.as_view(), name='serviced_person_detail'),
    path('serviced-persons', views.ServicedPersonListView.as_view(), name='serviced_person_list'),
    path('serviced-person/<int:pk_sp>/edit', views.ServicedPersonUpdateView.as_view(), name='serviced_person_update'),
    path('serviced-person/<int:pk_sp>/delete', views.ServicedPersonUpdateView.as_view(), name='serviced_person_delete'),

    # path('passport-data/create/<int:pk_sp>', views.PassportDataCreateView.as_view(), name='passport_data_create'),
    path('passport-data/<int:pk_pas>', views.PassportDataDetailView.as_view(), name='passport_data_detail'),
    path('passport-data/<int:pk_pas>/edit', views.PassportDataUpdateView.as_view(), name='passport_data_update'),

]
