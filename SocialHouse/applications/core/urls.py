from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('serviced_person/<pk_sp>', views.ServicedPersonDetailView.as_view(), name='serviced_person_detail'),
    path('passport_data/<pk_pas>', views.PassportDataDetailView.as_view(), name='passport_data_detail'),
]
