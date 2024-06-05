# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from ..home.models import Title
from django.http import JsonResponse
from django.middleware.csrf import get_token

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework import status
from django.contrib.auth.models import User
# ...

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")

            user = authenticate(request, username=username, password=raw_password)

            if user is not None:
                login(request, user)
                msg = 'User created and logged in successfully.'
                success = True
            else:
                msg = 'User creation successful, but login failed.'

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid Credentials'})

# ...

class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out."})

def csrf_token(request):
    # Generate CSRF token
    csrf_token = get_token(request)
    # Return CSRF token in JSON response
    return JsonResponse({'csrf_token': csrf_token})



from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password1 = request.data.get("password1")
        password2 = request.data.get("password2")

        if not username or not email or not password1 or not password2:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if password1 != password2:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, email=email, password=password1)

        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)