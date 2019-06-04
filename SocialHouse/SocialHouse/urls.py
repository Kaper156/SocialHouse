"""
SocialHouse URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from applications.core.views import profile
# from applications.core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('applications.core.urls')),
    path('news/', include('applications.news.urls'), ),
    path('accounts/profile/', profile)
]
