from django.contrib import messages
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'daphne',
    'silk',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    'channels',
    'smart_selects',
    'phonenumber_field',
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    #
    'acc',
    'person',
    'shop',
    'checkout',
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'answear.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'context_processors.context_processors.include_genders',
                'context_processors.context_processors.include_header_types',
                'context_processors.context_processors.include_brands',
                "dynamic_breadcrumbs.context_processors.breadcrumbs",
            ],
        },
    },
]

WSGI_APPLICATION = 'answear.wsgi.application'
ASGI_APPLICATION = 'answear.asgi.application'



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

MEDIA_ROOT = BASE_DIR / 'media_cdn'
MEDIA_URL = 'media/'
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

TEMP = BASE_DIR / 'media_cdn/temp'
LOGIN_REDIRECT_URL = 'shop:home'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'acc:login'
AUTH_USER_MODEL = "acc.CustomUser"
AUTHENTICATION_BACKENDS = ('acc.backends.EmailBackend',
                           'django.contrib.auth.backends.ModelBackend',
                           'allauth.account.auth_backends.AuthenticationBackend',
                           )

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }


SITE_ID = 1
CLIENT_ID = '649321607576-fkh7jo58sglu1c0jjpsifi6hqkbggjr2.apps.googleusercontent.com'
SECRET = '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'
KEY = ''
# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': CLIENT_ID,
            'secret': SECRET,
        }
    }
}

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

USE_DJANGO_JQUERY = True

try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *