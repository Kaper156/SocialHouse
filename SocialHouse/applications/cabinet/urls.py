from django.urls import path, include
from .views import ProfileView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('sw/', include('applications.social_work.urls')),
    # path('/ad/', include('applications.administrator_work.urls')),
]
