"""
Configuración para entorno de desarrollo
"""
from .base import *
from decouple import config

# #region agent log
import json
log_path = r"c:\TOTAL LIVING\.cursor\debug.log"
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"I","location":"total_living/settings/development.py:7","message":"development.py loading","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# #region agent log
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"I","location":"total_living/settings/development.py:13","message":"DEBUG and ALLOWED_HOSTS set","data":{"DEBUG":DEBUG,"ALLOWED_HOSTS":ALLOWED_HOSTS},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

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

# #region agent log
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"I","location":"total_living/settings/development.py:30","message":"Database configured","data":{"DB_PATH":DB_PATH},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

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

# #region agent log
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"I","location":"total_living/settings/development.py:50","message":"development.py loaded completely","data":{"ROOT_URLCONF":ROOT_URLCONF},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion
