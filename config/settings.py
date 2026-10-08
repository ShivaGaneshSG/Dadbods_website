"""
Django settings for DadBods Fitness Coaching Platform.
Production-ready configuration with environment variables and clean modular architecture.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# Security Settings
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dadbods-fitness-tamil-platform-secret-key-prod-ready-2026",
)
DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")

allowed_hosts_str = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver,*")
ALLOWED_HOSTS = ["*"] if DEBUG else [host.strip() for host in allowed_hosts_str.split(",") if host.strip()]

# Render external hostname support
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
if ".onrender.com" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(".onrender.com")

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "https://*.trycloudflare.com",
    "http://*.trycloudflare.com",
    "http://10.169.159.77:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Local Apps
    "core.apps.CoreConfig",
    "applications.apps.ApplicationsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # DadBods Context Processors
                "core.context_processors.dadbods_global_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database Configuration (SQLite for local dev, PostgreSQL-ready architecture)
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    import dj_database_url  # type: ignore # If installed in prod
    DATABASES = {"default": dj_database_url.config(default=DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media Files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Image Root for DadBods asset folder (D:/Dadbods/Website/images)
DADBODS_IMAGE_ROOT = Path(
    os.environ.get("DADBODS_IMAGE_ROOT", str(BASE_DIR / "images"))
)

# Configurable Coaching Investment / Budget Tiers
COACHING_BUDGET_CHOICES = [
    ("tier_premium", "₹10,000+ / month (Elite 1-on-1 Coaching)"),
    ("tier_standard", "₹7,000 – ₹10,000 / month (Standard Intensive)"),
    ("tier_core", "₹5,000 – ₹7,000 / month (Core Protocol)"),
    ("tier_entry", "₹3,500 – ₹5,000 / month (Essential Guidance)"),
    ("tier_budget", "Under ₹3,500 / month"),
]

# Email Notifications (Console Backend for Development)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ADMIN_NOTIFICATION_EMAIL = os.environ.get("ADMIN_NOTIFICATION_EMAIL", "team@dadbods.in")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "notifications@dadbods.in")

# YouTube API Configuration (Optional dynamic channel retrieval)
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")

# Static Files Storage with WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Production SSL & Reverse Proxy Settings (Render passes X-Forwarded-Proto)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").lower() in ("true", "1")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Primary Key Type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
