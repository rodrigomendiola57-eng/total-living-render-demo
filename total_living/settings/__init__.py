from decouple import config

# Determinar el entorno
ENVIRONMENT = config('ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'staging':
    from .staging import *
else:
    from .development import *
