from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from SocialHouse.views import DocsView

urlpatterns = [
    # path('', IndexView.as_view(), name='index'), # TODO add main page
    path('', RedirectView.as_view(url='/news/'), name='index'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico'), name='favicon'),
    path('admin/', admin.site.urls),  # admin site
    path('admin-tools/', include('admin_tools.urls')),  # admin site
    path('froala_editor/', include('froala_editor.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
    path('news/', include('applications.website.news.urls'), ),
    # path('', include('applications.core.urls')),
    path('lk/', include('applications.website.cabinet.urls')),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    path('laws/', DocsView.as_view(), name='laws')
]
