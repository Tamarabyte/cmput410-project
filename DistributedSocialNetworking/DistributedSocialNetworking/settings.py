"""
Django settings for DistributedSocialNetworking project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vqel$r-@3=j#f4dyakoaibpkys5&^l54!7=vl++4bu-7zs@cir'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


STATIC_ROOT = '/home/www/hindlebook/static'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'Hindlebook/static'),
)
STATIC_URL = '/static/'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'stream'

if DEBUG == True:
    MEDIA_ROOT = os.path.join(os.path.realpath(BASE_DIR), 'Hindlebook/media')
else:
    MEDIA_ROOT = '/home/www/hindlebook/media'

MEDIA_URL = "/media/"

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'widget_tweaks',
    'Hindlebook',
    'api'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'DistributedSocialNetworking.urls'

WSGI_APPLICATION = 'DistributedSocialNetworking.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'api.permissions.NodeAuthenticatedOrNotRequired'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.ForeignNodeAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ]
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Canada/Mountain'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s:  %(message)s',
        },
    },
    'handlers': {
        'file':{
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename' :  os.path.join(BASE_DIR, 'log.txt'),
        },
    },
    'loggers': {
        'custom': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'DEBUG',
        },
    }
}
