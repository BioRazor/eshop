from unipath import Path

#Devuelve la direccion del directorio raiz del proyecto
BASE_DIR = Path(__file__).ancestor(3)

SECRET_KEY = 'idknp-%0@t(*9hd@@$7*p6l9@71b5j5zqi%8tpto!w2%l*s%5@'

#Aplicaciones Locales
LOCAL_APPS = (
    'apps.administrativo',
    'apps.comercios',
    'apps.clientes',
	)

#Aplicaciones propias de django
DJANGO_APPS = (
        'grappelli',
		'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	)

#aplicaciones de terceros
THIRD_PARTY_APPS = (
    'ckeditor',    
	)

#Se le indican la aplicaciones instaladas a django
INSTALLED_APPS = THIRD_PARTY_APPS+ LOCAL_APPS + DJANGO_APPS 

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'eshop.urls'
WSGI_APPLICATION = 'eshop.wsgi.application'


#Se define el idioma del proyecto
LANGUAGE_CODE = 'es-es'

#Se define la zona horaria a utilizar
TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Se define la ruta de los archivos estaticos
STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR.child('static'),
    )

STATIC_ROOT = 'static'

AUTH_USER_MODEL = 'administrativo.Usuario'

CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'