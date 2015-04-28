from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'PORT': '5432',
        'NAME': 'social-auth',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'OPTIONS': {
            # "autocommit": True,
        },
    }
}

BASE_URL = "http://localhost:8000/"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'rdtcontacttree@gmail.com'
EMAIL_HOST_PASSWORD = 'invincible123#$'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '_temp/logs/app.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'WARNING',
        },
        '_main': {
            'handlers': ['file'],
            'level': 'WARNING',
        },
    }
}
