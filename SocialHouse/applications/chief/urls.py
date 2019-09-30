"""
SocialHouse URL Configuration
"""
from django.urls import path

from .views import ServicedPersonCreateView

urlpatterns = [
    path('serviced_persons', ServicedPersonCreateView.as_view(), name='url_serviced_persons_create')
]
