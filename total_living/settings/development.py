"""
Configuración para entorno de desarrollo
"""
from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Database - SQLite para desarrollo
# Usar ruta absoluta FIJA para evitar conflictos con otros proyectos
import os
# Forzar ruta absoluta del proyecto, sin importar desde dónde se ejecute
PROJECT_ROOT = r'C:\TOTAL LIVING'
DB_PATH = os.path.join(PROJECT_ROOT, 'db.sqlite3')
# Asegurar que la ruta sea absoluta
DB_PATH = os.path.abspath(DB_PATH)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_PATH,
    }
}

# Static files - WhiteNoise para desarrollo (solo si se necesita)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# En desarrollo, Django sirve los archivos estáticos automáticamente

# Email backend para desarrollo (consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
