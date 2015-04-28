from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

import dj_database_url
DATABASES = {}
DATABASES['default'] =  dj_database_url.config()

BASE_URL = "http://app.com/"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'rdtcontacttree@gmail.com'
EMAIL_HOST_PASSWORD = 'invincible123#$'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
