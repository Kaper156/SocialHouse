"""
SocialHouse URL Configuration
"""
from django.urls import path, include
from applications.news.views import news, post

urlpatterns = [
    # path('', news, name='news'),
    # path('<slug:slug_url>/', post, name='news_post'),
]
