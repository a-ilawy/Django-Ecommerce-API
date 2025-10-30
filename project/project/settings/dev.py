from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# $env:DJANGO_SETTINGS_MODULE="project.settings.dev"