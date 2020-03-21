from django.urls import path, include

from .views import ProfileView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('sw/', include('applications.social_work.providing.urls')),
    path('rt/', include('applications.receptionist.urls')),
]
