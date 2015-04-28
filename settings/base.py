
"""
Django settings for django_boilerplate project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n8f&s%8p_ul6qa#&n-3e8r*$71qq3y=8aqav0oevqklih1qh@d'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'bootstrap3',
    'rest_framework',
    'compressor',
    'apps.account',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'apps.account.middleware.ProcessUserLayout',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = ( 
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

APP_NAME = "App_Name"

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'apps.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

AUTH_USER_MODEL = 'account.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

TIME_FORMAT = "%d %b %Y T %X"
DATE_FORMAT = "%Y-%m-%d"

TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',
 'django.template.loaders.app_directories.Loader')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGIN_URL = '/login'

GRAPPELLI_ADMIN_TITLE = APP_NAME 
