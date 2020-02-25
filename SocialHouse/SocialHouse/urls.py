from django.contrib import admin
from django.urls import path, include
import admin_tools

urlpatterns = [
    path('admin/', admin.site.urls),  # admin site
    path('admin-tools/', include('admin_tools.urls')),  # admin site
    path('accounts/', include('django.contrib.auth.urls')),
    path('news/', include('applications.news.urls'), ),
    path('', include('applications.core.urls')),
    path('lk/', include('applications.cabinet.urls')),
]
