from .base import *

DEBUG = True

# ALLOWED_HOSTS = ['*']

import dj_database_url
DATABASES = {}
DATABASES['default'] =  dj_database_url.config()

BASE_URL = "http://tutio.com/"
