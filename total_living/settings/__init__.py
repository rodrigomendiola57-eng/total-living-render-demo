# #region agent log
import json
import os
log_path = r"c:\TOTAL LIVING\.cursor\debug.log"
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"F","location":"total_living/settings/__init__.py:5","message":"Settings __init__ loading","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

from decouple import config
import os

# Determinar el entorno
ENVIRONMENT = config('ENVIRONMENT', default='development')

# #region agent log
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"F","location":"total_living/settings/__init__.py:12","message":"Environment determined","data":{"ENVIRONMENT":ENVIRONMENT},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

if ENVIRONMENT == 'production':
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"F","location":"total_living/settings/__init__.py:17","message":"Loading production settings","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    except: pass
    # #endregion
    from .production import *
elif ENVIRONMENT == 'staging':
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"F","location":"total_living/settings/__init__.py:24","message":"Loading staging settings","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    except: pass
    # #endregion
    from .staging import *
else:
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"F","location":"total_living/settings/__init__.py:31","message":"Loading development settings","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    except: pass
    # #endregion
    from .development import *

# #region agent log
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"F","location":"total_living/settings/__init__.py:35","message":"Settings loaded","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion
