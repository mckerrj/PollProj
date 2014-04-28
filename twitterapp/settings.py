"""
Django settings for twitterapp project.

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
SECRET_KEY = '@w_ia9+*-o@pdgueo*n2ts4hr%3_&=l)!0ag5bg3%ght7=g&k-'

# Security stuff for Twitter API, and screen name.
OAUTH_TOKEN = '15764888-ukDfMEmRZlvuIkDwWo80tRCcCtmfED98iVkCdNOoL'
OAUTH_TOKEN_SECRET = 'THyPnDcmTAt0K7clLAIbm0vVQRN1GbL3DcsvrDutEKdLt'
CONSUMER_KEY = 'nEi0sMZ6kQniAJoBJv9GvSxgT'
CONSUMER_SECRET = '0u1oZ0mxXMlrYSNTdyHH1U3WBFpKaFBLGOZLKPv2r4ULbAoxeM'
TWITTER_SCREENNAME = 'kleids'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'twitter',
    'tastypie',
    'provider',
    'provider.oauth2',
    'djcelery'
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'twitterapp.urls'

WSGI_APPLICATION = 'twitterapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'twitter',
        'USER': 'twitter',
        'PASSWORD': 'twitter314',
        'HOST': '192.168.33.10',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
#STATICFILES_DIRS = ('/static/',)
STATIC_ROOT = '/static/'
API_LIMIT_PER_PAGE = 20

TASTYPIE_DEFAULT_FORMATS = ['json']

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'twitter/tests/fixtures'),
)

# Celery stuff
BROKER_URL = 'redis://192.168.33.10:6379/0'
CELERY_RESULT_BACKEND = 'redis://192.168.33.10:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']  # Ignore other content
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True

from datetime import timedelta
from celery.schedules import crontab

# Showing timedelta and crontab style
# more docos here: http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'twitter.tasks.add',
        'schedule': timedelta(seconds=30),
        'args': (16, 16)
    },
    'hello-every-10-seconds': {
        'task': 'twitter.tasks.hello',
        'schedule': timedelta(seconds=10)
    },
    'run-twitter-sync-every-5-minutes': {
        'task': 'twitter.tasks.run_twitter_sync',
        'schedule': crontab(minute='*/1')
    },
}