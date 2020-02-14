from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('admin/', admin.site.urls),  # admin site
    # path('login/', 'django.contrib.auth.views.login', name="login"),
    # path('login/', LoginView, name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('news/', include('applications.news.urls'), ),
    path('', include('applications.core.urls')),
    path('lk/', include('applications.cabinet.urls')),

]
