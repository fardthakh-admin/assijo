# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# load production server from .env
ALLOWED_HOSTS = ["localhost", "127.0.0.1", config('SERVER', default='localhost'), '10.239.181.28', '10.0.2.2', "agritech-jo.com",
    "www.agritech-jo.com",]

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication', 
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         # 'rest_framework.permissions.IsAuthenticated',
#         # other permissions as needed
#     ],
# }

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         # "rest_framework.authentication.TokenAuthentication",
#         # 'rest_framework.authentication.BasicAuthentication',
#         # 'rest_framework.authentication.SessionAuthentication',
#         # 'rest_framework_simplejwt.authentication.JWTAuthentication',
#         # other authentication classes as needed
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         # 'rest_framework.permissions.IsAuthenticated',
#         # other permissions as needed
#     ],
# }


# SIMPLE_JWT = {
#     'BLACKLIST_AFTER_ROTATION': True,
#     'UPDATE_LAST_LOGIN': True,
# }
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    "django.contrib.sites",

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.home',  # Enable the inner home (home)
    'restapi.apps.RestapiConfig',

    'rest_framework',
    'rest_framework.authtoken',


    "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    
    # "rest",
    # "dj_rest_auth",
    # "dj_rest_auth.registration",

    'numpy',
]

AUTH_USER_MODEL = 'home.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.home.views.DisableCsrfCheck'
]
ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = 'optional'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }    path('login/',LoginView.as_view(template_name="accounts/login.html"),  name="login"),

# }
DATABASES = {
     "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": "localhost",
        "PORT": 5432,
        "NAME": "assijo",
        "USER": "elabbasy",
        "PASSWORD": "elabbasy",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),

)
# CSRF_COOKIE_SECURE = False

# CSRF_COOKIE_HTTPONLY = True

CSRF_TRUSTED_ORIGINS = ['http://localhost:8000','http://10.0.2.2:8000']

SITE_ID = 1

FORCE_SCRIPT_NAME = '/assissjo-api'
# AUTHENTICATION_BACKENDS={

#     "django.contrib.auth.backends.ModelBackend",
#     "allauth.account.auth_backends.AuthenticationBackend",


# }

# REST_AUTH = {
#  'LOGIN_SERIALIZER': 'dj_rest_auth.serializers.LoginSerializer',
#     'TOKEN_SERIALIZER': 'dj_rest_auth.serializers.TokenSerializer',
#     'JWT_SERIALIZER': 'dj_rest_auth.serializers.JWTSerializer',
#     'JWT_SERIALIZER_WITH_EXPIRATION': 'dj_rest_auth.serializers.JWTSerializerWithExpiration',
#     'JWT_TOKEN_CLAIMS_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer',
#     'USER_DETAILS_SERIALIZER': 'dj_rest_auth.serializers.UserDetailsSerializer',
# #     'PASSWORD_RESET_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetSerializer',
#     'PASSWORD_RESET_CONFIRM_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetConfirmSerializer',
#     'PASSWORD_CHANGE_SERIALIZER': 'dj_rest_auth.serializers.PasswordChangeSerializer',

    # 'REGISTER_SERIALIZER': 'dj_rest_auth.registration.serializers.RegisterSerializer',

#     'REGISTER_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),

    # 'TOKEN_MODEL': 'rest_framework.authtoken.models.Token',
    # 'TOKEN_CREATOR': 'dj_rest_auth.utils.default_create_token',

#     'PASSWORD_RESET_USE_SITES_DOMAIN': False,
#     'OLD_PASSWORD_FIELD_ENABLED': False,
#     'LOGOUT_ON_PASSWORD_CHANGE': False,
#     'SESSION_LOGIN': True,
#     'USE_JWT': False,

#     'JWT_AUTH_COOKIE': None,
#     'JWT_AUTH_REFRESH_COOKIE': None,
#     'JWT_AUTH_REFRESH_COOKIE_PATH': '/',
#     'JWT_AUTH_SECURE': False,
#     'JWT_AUTH_HTTPONLY': True,
#     'JWT_AUTH_SAMESITE': 'Lax',
#     'JWT_AUTH_RETURN_EXPIRATION': False,
#     'JWT_AUTH_COOKIE_USE_CSRF': False,
#     'JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED': False,
# }
#############################################################
#############################################################
