"""
Configuración para PythonAnywhere (prueba)
"""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Base de datos SQLite para prueba
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = '/home/yourusername/total_living/staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/yourusername/total_living/media'