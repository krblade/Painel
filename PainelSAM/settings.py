"""
Django settings for PainelSAM project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import locale

locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true" 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PainelSAM.settings')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*^02*e66=7h7#r^47n0_8_y)2)*5l0q&37^e_9zr)k9agzzuoy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.163.152.165', '127.0.0.1', 'localhost', 'mi00311557','192.168.1.90']


# Application definition

INSTALLED_APPS = [
  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'paginas',
    'registros',
    'django_extensions',
    'ckeditor',
    'ckeditor_uploader'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]

MIDDLEWARE_CLASSES = (
    'reversion.middleware.RevisionMiddleware',
)

ROOT_URLCONF = 'PainelSAM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'user_tags':'paginas.templatetags.user_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'PainelSAM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'db_gopi_sam',
#         'USER': 'DB_GOPI_SAM',
#         'PASSWORD': 'sam_GOPI@2021',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.oracle',
#        'NAME': 'DB_GOPI_SAM',
#        #'NAME': 'xe',
#        'USER': 'DB_GOPI_SAM',
#        'PASSWORD': 'sam_GOPI@2021',
#        'HOST': 'MI00311266',
#        'PORT': '1521',
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_TZ = False
USE_I18N = True
USE_L10N = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL ='/media/'
MEDIA_ROOT = 'media/'
CKEDITOR_UPLOAD_PATH = ('uploads/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'inicio'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'

SESSION_EXPIRE_SECONDS = 36000
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
#SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 1
SESSION_TIMEOUT_REDIRECT = 'inicio'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT =  587
EMAIL_USE_TLS = True
EMAIL_HOST_USER ='admsistemasam@gmail.com'
EMAIL_HOST_PASSWORD ='fabiana21' 

