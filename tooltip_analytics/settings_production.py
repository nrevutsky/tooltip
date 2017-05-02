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

