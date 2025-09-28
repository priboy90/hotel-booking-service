"""
Конфигурация Django с использованием Pydantic Settings.
"""

import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DjangoSettings(BaseSettings):
    """
    Настройки Django с валидацией через Pydantic.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    # Базовые настройки Django
    DEBUG: bool = True
    SECRET_KEY: str = "django-insecure-change-in-production-please!"
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "0.0.0.0"]

    # База данных
    DATABASE_URL: PostgresDsn = "postgresql://user:password@localhost:5432/hotel_booking_db"

    # Международные настройки
    LANGUAGE_CODE: str = "ru-ru"
    TIME_ZONE: str = "Europe/Moscow"
    USE_I18N: bool = True
    USE_TZ: bool = True

    # Статические файлы
    STATIC_URL: str = "/static/"

    @property
    def DATABASES(self) -> dict[str, Any]:
        """
        Динамически создаем конфигурацию базы данных из DATABASE_URL.
        """
        # Используем метод unicode_string() для получения строки URL
        db_url_str = self.DATABASE_URL.unicode_string()
        parsed = urlparse(db_url_str)

        username = parsed.username or "booking_user"
        password = parsed.password or "strong_password_123!"
        hostname = parsed.hostname or "localhost"
        port = parsed.port or 5432
        database = parsed.path.lstrip("/") or "hotel_booking_db"

        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": database,
                "USER": username,
                "PASSWORD": password,
                "HOST": hostname,
                "PORT": port,
            }
        }

    @field_validator("ALLOWED_HOSTS", mode="before")
    def parse_allowed_hosts(cls, v):
        """Парсим ALLOWED_HOSTS из строки в список."""
        if isinstance(v, str):
            # Пробуем парсить как JSON
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # Если не JSON, разбиваем по запятым
                return [host.strip() for host in v.split(",") if host.strip()]
        return v

    @field_validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        """Проверяем, что секретный ключ достаточно сложный."""
        if v == "django-insecure-change-in-production-please!":
            print("⚠️  ВНИМАНИЕ: Используется стандартный SECRET_KEY. ЗАМЕНИТЕ В ПРОДАКШЕНЕ!")
        elif len(v) < 20:
            raise ValueError("SECRET_KEY должен быть не менее 20 символов")
        return v


# Создаем экземпляр настроек
settings = DjangoSettings()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings.DEBUG

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Наши приложения
    "rest_framework",
    "rooms",
    "bookings",
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

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "core.wsgi.application"

# Database
DATABASES = settings.DATABASES

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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
LANGUAGE_CODE = settings.LANGUAGE_CODE
TIME_ZONE = settings.TIME_ZONE
USE_I18N = settings.USE_I18N
USE_TZ = settings.USE_TZ

# Static files
STATIC_URL = settings.STATIC_URL

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
}
