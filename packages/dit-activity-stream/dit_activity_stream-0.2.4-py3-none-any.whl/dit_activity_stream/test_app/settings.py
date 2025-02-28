import os

import django.utils.crypto

ALLOWED_HOSTS = ["localhost"]

TESTS_PATH = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = django.utils.crypto.get_random_string(50)

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "dit_activity_stream",
    "dit_activity_stream.test_app.apps.TestAppConfig",
]

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
            ],
        },
    },
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

MEDIA_ROOT = os.path.join(TESTS_PATH, "media")

STATIC_ROOT = os.path.join(TESTS_PATH, "static")

ROOT_URLCONF = "dit_activity_stream.test_app.urls"

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
]

AUTH_USER_MODEL = "dit_activity_stream_test_app.CustomUser"

# Django HAWK settings
DJANGO_HAWK = {
    "HAWK_INCOMING_ACCESS_KEY": "xxx",
    "HAWK_INCOMING_SECRET_KEY": "xxx",
}

# DIT Activity Stream settings
DIT_ACTIVITY_STREAM_CLIENT_CLASS = (
    "dit_activity_stream.test_app.client.TestActivityStreamClient"
)
