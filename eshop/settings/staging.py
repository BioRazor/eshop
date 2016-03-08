#local.py
#Se importan todas las configuraciones del archivo base.py 
from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd1u7fj82igoomm',
        'USER': 'qivxttzczsbeug',
        'PASSWORD': 'Y3pIBSgeFE4I_9TWAILR2xvcUD',
        'HOST': 'ec2-54-227-246-11.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (BASE_DIR.child('static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')