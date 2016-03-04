#local.py
#Se importan todas las configuraciones del archivo base.py 
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dpgcgdvdkfcv5',
        'USER': 'zimaoonsxbdvmf',
        'PASSWORD': 'I3XvmG80dyV0asU9Kej40cnyf_',
        'HOST': 'ec2-54-227-250-148.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}
"""
#Se definae la ruta y la carpeta en la que se guardaran los archivos MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')