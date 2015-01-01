from .base import *

DEBUG = True

# ALLOWED_HOSTS = ['*']

import dj_database_url
DATABASES['default'] =  dj_database_url.config()