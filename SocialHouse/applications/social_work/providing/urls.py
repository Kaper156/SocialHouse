"""
SocialHouse URL Configuration
"""
from django.urls import path

from .views import ServiceJournalCreateView

urlpatterns = [
    path('services_journals', ServiceJournalCreateView.as_view(), name='url_services_journals_create')
]
