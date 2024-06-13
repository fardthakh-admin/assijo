# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import register_user
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('login/',LoginView.as_view(template_name="accounts/login.html"),  name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
