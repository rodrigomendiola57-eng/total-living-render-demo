#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# #region agent log
import json
log_path = r"c:\TOTAL LIVING\.cursor\debug.log"
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"L","location":"manage.py:8","message":"manage.py starting","data":{"cwd":os.getcwd(),"script":__file__},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

def main():
    """Run administrative tasks."""
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"L","location":"manage.py:15","message":"main() called","data":{"args":sys.argv},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    except: pass
    # #endregion
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'total_living.settings.development')
    
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"L","location":"manage.py:22","message":"DJANGO_SETTINGS_MODULE set in manage.py","data":{"module":os.environ.get('DJANGO_SETTINGS_MODULE')},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    except: pass
    # #endregion
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"L","location":"manage.py:33","message":"About to execute command","data":{"command":sys.argv},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    except: pass
    # #endregion
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
