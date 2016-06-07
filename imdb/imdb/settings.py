# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SYNOPSIS = os.path.abspath(BASE_DIR+"/../synopsis/")
STORYLINE = os.path.abspath(BASE_DIR+"/../storyline/")

SECRET_KEY = 'rn-qzjz8gh4l@!_wc-5@($x@qo910p@-og2t@4udv#4i0#cb(s'

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASE = {
    'ENGINE': "django.db.backends.mysql",
    'NAME': 'IMDB',
    'USER': 'root',
    'PASSWORD': '1234',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'ATOMIC_REQUESTS': True,
}

DATABASES = {
    'default': DATABASE
}

INSTALLED_APPS = [
    'serverapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'imdb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',       
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'imdb.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
