from settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tooltipdb',
        'USER': 'tooltip_user',
        'PASSWORD': 'tooltippass',
        'HOST': 'localhost',
        'PORT': '',
    }
}

BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
