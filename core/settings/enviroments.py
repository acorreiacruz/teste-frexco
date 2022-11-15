import os
from pathlib import Path
from typing import List


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = 1 if os.environ.get("DEBUG") == "1" else 0

ALLOWED_HOSTS: List[str] = []

ROOT_URLCONF = "core.urls"

WSGI_APPLICATION = "core.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
