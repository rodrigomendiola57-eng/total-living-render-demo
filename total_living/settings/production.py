"""
Configuración para entorno de producción (AWS)
"""
from .base import *
from decouple import config
from django.core.exceptions import ImproperlyConfigured
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = [h.strip() for h in config('ALLOWED_HOSTS', default='').split(',') if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in config('CSRF_TRUSTED_ORIGINS', default='').split(',') if o.strip()]

if not ALLOWED_HOSTS:
    raise ValueError('ALLOWED_HOSTS debe configurarse en producción.')

# Database - PostgreSQL en AWS RDS
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Security settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=SECURE_SSL_REDIRECT, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=SECURE_SSL_REDIRECT, cast=bool)
SESSION_COOKIE_SAMESITE = config('SESSION_COOKIE_SAMESITE', default='Lax')
CSRF_COOKIE_SAMESITE = config('CSRF_COOKIE_SAMESITE', default='Lax')
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# En producción real conviene activarlo para bloquear claves débiles.
ENFORCE_STRONG_SECRET_KEY = config('ENFORCE_STRONG_SECRET_KEY', default=False, cast=bool)
if ENFORCE_STRONG_SECRET_KEY:
    weak_key = (
        not SECRET_KEY
        or SECRET_KEY.startswith('django-insecure-')
        or len(SECRET_KEY) < 50
        or len(set(SECRET_KEY)) < 5
    )
    if weak_key:
        raise ImproperlyConfigured(
            'SECRET_KEY insegura: usa una clave aleatoria robusta y >= 50 caracteres.'
        )

if not DEBUG:
    # Nota: SECURE_BROWSER_XSS_FILTER es un ajuste legacy para navegadores antiguos.
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# AWS S3 Storage para archivos estáticos y media (opcional por entorno)
USE_S3 = config('USE_S3', default=False, cast=bool)

if USE_S3:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_STATIC_LOCATION = config('AWS_STATIC_LOCATION', default='static')
    AWS_MEDIA_LOCATION = config('AWS_MEDIA_LOCATION', default='media')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = None

    # Static files
    STATICFILES_STORAGE = 'total_living.storage_backends.StaticStorage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/'

    # Media files
    DEFAULT_FILE_STORAGE = 'total_living.storage_backends.MediaStorage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/'
else:
    # Modo contenedor local / predeploy sin AWS.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER or 'no-reply@example.com')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
