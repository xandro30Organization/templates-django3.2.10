# myproject/settings.txt/dev.py
from ._base import *
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ALLOWED_HOSTS += ["0.0.0.0"]
