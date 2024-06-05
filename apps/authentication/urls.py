# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import register_user
from django.contrib.auth.views import LogoutView, LoginView
from .views import csrf_token
from .views import LoginAPIView, LogoutAPIView, RegisterAPIView
urlpatterns = [
    path('login/',LoginView.as_view(template_name="accounts/login.html"),  name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('api/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    
]