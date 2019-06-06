"""
SocialHouse URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

from applications.core.views import profile

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('login/', 'django.contrib.auth.views.login', name="login"),
    # path('login/', LoginView, name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('news/', include('applications.news.urls'), ),
    path('profile/', profile, name='profile'),
    path('', include('applications.core.urls')),

]
