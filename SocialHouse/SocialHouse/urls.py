from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from SocialHouse.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico'), name='favicon'),
    path('admin/', admin.site.urls),  # admin site
    path('admin-tools/', include('admin_tools.urls')),  # admin site
    path('accounts/', include('django.contrib.auth.urls')),
    path('news/', include('applications.website.news.urls'), ),
    # path('', include('applications.core.urls')),
    path('lk/', include('applications.website.cabinet.urls')),
]
