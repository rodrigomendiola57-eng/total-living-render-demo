"""
Configuración base compartida para todos los entornos
"""
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Para formateo de números (intcomma)
    
    # Apps locales
    'properties',
    'accounts',
    'contact',
    'search',
    'panel',
    'developments',
    'regions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'total_living.middleware_no_cache.NoCacheHTMLMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'total_living.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'total_living.context_processors.map_tiles',
            ],
        },
    },
]

WSGI_APPLICATION = 'total_living.wsgi.application'

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'es-es'
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
]
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Map tiles provider (production-ready, configurable via .env)
# Examples:
# MAP_TILE_URL=https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png
# MAP_TILE_ATTRIBUTION=&copy; OpenStreetMap contributors
# MAP_TILE_SUBDOMAINS=abc
# MAP_TILE_MAX_ZOOM=19
MAP_TILE_URL = config('MAP_TILE_URL', default='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png')
MAP_TILE_ATTRIBUTION = config(
    'MAP_TILE_ATTRIBUTION',
    default='&copy; OpenStreetMap contributors &copy; CARTO'
)
MAP_TILE_SUBDOMAINS = config('MAP_TILE_SUBDOMAINS', default='abcd')
MAP_TILE_MAX_ZOOM = config('MAP_TILE_MAX_ZOOM', default=20, cast=int)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Caché (login del panel: rate limit; con varios workers Gunicorn,
# considera Redis/Memcached para límites globales coherentes).
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'total-living-default-cache',
    }
}

# Límite de intentos POST al login del panel: ej. "15/15m", "5/m", "10/h"
PANEL_LOGIN_RATELIMIT_IP = config('PANEL_LOGIN_RATELIMIT_IP', default='15/15m')
PANEL_LOGIN_RATELIMIT_USERNAME = config('PANEL_LOGIN_RATELIMIT_USERNAME', default='8/15m')

# Límite de envíos POST al formulario público de contacto (por IP).
# Ajusta según tráfico real. Ejemplo: "10/10m" o "30/h".
CONTACT_FORM_RATELIMIT_IP = config('CONTACT_FORM_RATELIMIT_IP', default='5/h')

# Rutas privadas de acceso administrativo (incluye slash final).
# Puedes sobrescribirlas por entorno con variables .env.
ADMIN_URL_PATH = config('ADMIN_URL_PATH', default='gestion-total-living-2026/')
PANEL_URL_PATH = config('PANEL_URL_PATH', default='acceso-interno-staff-2026/')

# Solo para pruebas locales/predeploy con Docker: servir MEDIA desde Django
# aun cuando DEBUG=False. En producción real mantenerlo en False y usar S3/CDN.
SERVE_LOCAL_MEDIA = config('SERVE_LOCAL_MEDIA', default=False, cast=bool)
