from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-8a=7%)ji2h1tugija%c10_m)l(7jdi^r2q40ikpq^9c'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'answear',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static',
                    BASE_DIR / 'media', ]
STATIC_ROOT = BASE_DIR /'static_cdn'
