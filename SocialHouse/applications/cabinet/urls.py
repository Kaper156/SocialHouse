"""
SocialHouse URL Configuration
"""
from django.urls import path, include

urlpatterns = [
    path('sw/', include('applications.social_work.urls')),
    # path('/ad/', include('applications.administrator_work.urls')),
]
