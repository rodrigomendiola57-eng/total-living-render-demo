"""
Configuración base compartida para todos los entornos
"""
from pathlib import Path
from decouple import config
import os

# #region agent log
log_path = r"c:\TOTAL LIVING\.cursor\debug.log"
try:
    import json
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"G","location":"total_living/settings/base.py:10","message":"base.py loading","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# #region agent log
try:
    import json
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"G","location":"total_living/settings/base.py:17","message":"BASE_DIR calculated","data":{"BASE_DIR":str(BASE_DIR)},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

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

# #region agent log
try:
    import json
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"G","location":"total_living/settings/base.py:42","message":"INSTALLED_APPS configured","data":{"apps":INSTALLED_APPS},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'total_living.urls'

# #region agent log
try:
    import json
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"G","location":"total_living/settings/base.py:58","message":"ROOT_URLCONF set","data":{"ROOT_URLCONF":ROOT_URLCONF},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

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

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# #region agent log
try:
    import json
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"G","location":"total_living/settings/base.py:105","message":"base.py loaded completely","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion
