from django.urls import path

import applications.serviced_data.views

urlpatterns = [
    # path('passport-data/create/<int:pk_sp>', views.PassportDataCreateView.as_view(), name='passport_data_create'),
    path('passport-data/<int:pk_pas>', applications.serviced_data.views.PassportDataDetailView.as_view(),
         name='passport_data_detail'),
    path('passport-data/<int:pk_pas>/edit', applications.serviced_data.views.PassportDataUpdateView.as_view(),
         name='passport_data_update'),
]
