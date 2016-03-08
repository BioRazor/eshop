#local.py
#Se importan todas las configuraciones del archivo base.py 
from .base import *

DEBUG = True

ALLOWED_HOSTS = []

#Configuracion de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR.child('static'),)
#Se definae la ruta y la carpeta en la que se guardaran los archivos MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')

THIRD_PARTY_APPS = (
		'debug_toolbar',		
	)

INSTALLED_APPS += THIRD_PARTY_APPS

DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CLASSES = (
	'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)