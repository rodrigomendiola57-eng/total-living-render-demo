"""
WSGI config for total_living project.
"""
import os

# #region agent log
import json
log_path = r"c:\TOTAL LIVING\.cursor\debug.log"
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"H","location":"total_living/wsgi.py:8","message":"WSGI module loading","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'total_living.settings.production')

# #region agent log
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"H","location":"total_living/wsgi.py:16","message":"DJANGO_SETTINGS_MODULE set","data":{"module":os.environ.get('DJANGO_SETTINGS_MODULE')},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

application = get_wsgi_application()

# #region agent log
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"H","location":"total_living/wsgi.py:22","message":"WSGI application created","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion
