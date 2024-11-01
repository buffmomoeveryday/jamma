from pathlib import Path

from decouple import config
from django.shortcuts import reverse

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=True, cast=bool)

IP_INFO_TOKEN = config("IP_INFO_TOKEN")


# Application definition
USER_APPS = [
    "track",
    "landing",
]

THIRD_PARTY_APPS = [
    # cors
    "corsheaders",
    # celery results
    "django_celery_results",
    "django_celery_beat",
    "django_extensions",
    # debug
    "silk",
    "debug_toolbar",
    # websockets
    "channels",
    # htmx
    "django_htmx",
    # rest frameowrk
    "rest_framework",
    # slippers
    "slippers",
    # widget tweaks
    "widget_tweaks",
    # filter
    "django_filters",
]

INSTALLED_APPS = [
    # custom user
    "user",
    # channels
    "daphne",
    # event stream
    "django_eventstream",
    # django's own
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS += USER_APPS
INSTALLED_APPS += THIRD_PARTY_APPS


MIDDLEWARE = [
    # custom middleware: host validation, session middleware for recording session
    # "core.middleware.hostvalidation.HostValidationMiddleware",
    # django middlewares
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # cors middlewares
    "corsheaders.middleware.CorsMiddleware",
    # django middleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "core.middleware.list_of_available_websites.WebsiteListMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # django debug toolbar
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    # silk middleware
    "silk.middleware.SilkyMiddleware",
    # htmx middleware
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "landing.context_processors.websites",
            ],
            "builtins": [
                "slippers.templatetags.slippers",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                ("127.0.0.1", 6379),
            ],
        },
    },
}

# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "postgres",
#         "USER": "postgres.ciwvvgjwebvhjtwefirl",
#         "PASSWORD": "b0WRRn0CZRkjrwtM",
#         "HOST": "aws-0-us-east-1.pooler.supabase.com",
#         "PORT": "6543",
#     }
# }


# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "static/"

# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# CORS
ALLOWED_HOSTS = ["*"]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8001",
    "https://jamma.buffmomo.xyz",
    "https://share.siddharthakhanal.com",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [
    "https://jamma.buffmomo.xyz",
    "http://192.168.101.6:5174",
    "https://share.siddharthakhanal.com",
]

# celery
CELERY_CACHE_BACKEND = "django-cache"
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kathmandu"
CELERY_RESULT_BACKEND = "django-db"

# celery beat
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# custom settings
AUTH_USER_MODEL = "user.User"
LOGIN_REDIRECT_URL = "/"

# debug
INTERNAL_IPS = [
    "127.0.0.1",
    "https://jamma.buffmomo.xyz/",
]

# silk
SILKY_PYTHON_PROFILER = True
SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True
# not supported by sqlite3
# SILKY_ANALYZE_QUERIES = True

# session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


# settings.py

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#         },
#         "myapp": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#             "propagate": True,
#         },
#     },
# }