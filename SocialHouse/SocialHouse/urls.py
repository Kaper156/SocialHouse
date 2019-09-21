from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('login/', 'django.contrib.auth.views.login', name="login"),
    # path('login/', LoginView, name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('news/', include('applications.news.urls'), ),
    path('', include('applications.core.urls')),
    path('lk/', include('applications.cabinet.urls')),

]
