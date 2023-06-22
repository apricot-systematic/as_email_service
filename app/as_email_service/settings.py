"""
Django settings for as_email_service project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
# System imports
#
from pathlib import Path
from typing import List

# 3rd party imports
#
import environ

# This is be "/app" inside the docker container.
#
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = environ.Path(__file__) - 3

env = environ.Env(DEBUG=(bool, False))

# Read various parts of the configuration from the environment.
#
env.read_env(BASE_DIR(".env"))

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")
SITE_NAME = env("SITE_NAME")

ALLOWED_HOSTS: List[str] = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "anymail",
    "django_extensions",
    "huey.contrib.djhuey",
    "ordered_model",
    "as_email",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "as_email_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "as_email_service.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {"default": env.db()}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Los_Angeles"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

HUEY = {
    "huey_class": "huey.SqliteHuey",
    "name": "as_email_service",
    "immediate": False,
    "results": True,  # Store return values of tasks.
    "utc": True,  # Use UTC for all times internally.
    "filename": env("HUEY_DB_FILE"),
    "consumer": {
        "workers": 4,
        "worker_type": "thread",
        "scheduler_interval": 1,  # Check schedule every second, -s.
        "periodic": True,  # Enable crontab feature.
        "check_worker_health": True,  # Enable worker health checks.
    },
}

DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="AS Email Service <noreply@apricot.com>",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[AS Email Service]",
)

# If EMAIL_BACKEND is set, configure anymail. Otherwise use `EMAIL_HOST`
if "EMAIL_BACKEND" in env:
    EMAIL_BACKEND = env("EMAIL_BACKEND")
    ANYMAIL = env.dict("ANYMAIL")
else:
    # https://docs.djangoproject.com/en/dev/ref/settings/#email-host
    EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
    # https://docs.djangoproject.com/en/dev/ref/settings/#email-port
    EMAIL_PORT = 1025

# A dict of the tokens for access to the postmark mail 'server's. The
# key is the name of the server at postmark, and the value is the
# server token for that server.
#
EMAIL_SERVER_TOKENS = env.dict("EMAIL_SERVER_TOKENS")
EMAIL_SPOOL_DIR = Path(env("EMAIL_SPOOL_DIR"))
