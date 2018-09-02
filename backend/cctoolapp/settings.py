"""
Django settings for cctoolapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
from django.utils.crypto import get_random_string

# Live environment or not.
mode = os.environ.get('RUN_MODE', '')

BASE_DIR      = os.path.dirname( os.path.dirname(__file__) )
TEMPLATE_DIRS = [ os.path.join(BASE_DIR, 'templates') ]
STATIC_URL    = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = []
ROOT_URLCONF  = 'cctoolapp.urls'
WSGI_APPLICATION = 'cctoolapp.wsgi.application'

# SECURITY WARNING: keep the secret key used in production secret!
# For extra security, it is randomly generated.
SECRET_KEY = os.environ.get("SECRET_KEY", get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"))

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'cctool',
	'rest_framework',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DATABASES = {
	'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'cctooldb',
			'USER': 'postgres',
			'PASSWORD': 'postgres',
			'HOST': 'cctool-dev-db',
			'PORT': 5432,
		}
}

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'class': 'common.lib.logging.et_logging.ETLogFormatter',
			'format': '%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s',
		},
	},
	'handlers': {
		'debug_log': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': os.path.join(BASE_DIR, 'logs/webapp.log.dg'),
			'maxBytes': 2000000,
			'backupCount': 5,
			'formatter': 'verbose',
		},
		'info_log': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': os.path.join(BASE_DIR, 'logs/webapp.log'),
			'maxBytes': 2000000,
			'backupCount': 3,
			'formatter': 'verbose',
		},
		'error_log': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': os.path.join(BASE_DIR, 'logs/webapp.log.wf'),
			'maxBytes': 2000000,
			'backupCount': 3,
			'formatter': 'verbose',
		},
	},
	'loggers':{
		'cctoolapp': {
		'handlers': ['debug_log', 'info_log', 'error_log'],
		'level': 'DEBUG',
		'propagate': False,
		},
	}
}
# SECURITY WARNING: don't run with debug turned on in production!
if mode == 'prod':
	DEBUG = False
	TEMPLATE_DEBUG = False
	ALLOWED_HOSTS = ['*']
else:
	DEBUG = True
	TEMPLATE_DEBUG = True
	ALLOWED_HOSTS = []

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
	'PAGINATE_BY': 1000
}
