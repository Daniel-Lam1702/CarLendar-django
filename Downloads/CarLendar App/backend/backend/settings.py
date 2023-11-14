from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
#Adding the firebase configuration
import firebase_admin
from firebase_admin import credentials
"""SETUP FIREBASE CREDENTIALS"""
cred = credentials.Certificate({
        "type" : os.environ.get('FIREBASE_ACCOUNT_TYPE'),
        "project_id" : os.environ.get('FIREBASE_PROJECT_ID'),
        "private_key_id" : os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
        "private_key" : os.environ.get('FIREBASE_PRIVATE_KEY'),
        "client_email" : os.environ.get('FIREBASE_CLIENT_EMAIL'),
        "client_id" : os.environ.get('FIREBASE_CLIENT_ID'),
        "auth_uri" : os.environ.get('FIREBASE_AUTH_URI'),
        "token_uri" : os.environ.get('FIREBASE_TOKEN_URI'),
        "auth_provider_x509_cert_url" : os.environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url" : os.environ.get('FIREBASE_CLIENT_X509_CERT_URL'),
        "universe_domain": os.environ.get('UNIVERSE_DOMAIN'),
})
default_app = firebase_admin.initialize_app(cred)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'your_project_name.path.to.CustomAuthentication',  # Replace with the actual path
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'usercar',
    'posts',
    'cars',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'corsheaders',
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
    ),
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'carlendar',
        'USER': 'root',
        'HOST': 'localhost',  # or the IP address of your MySQL server
        'PORT': '3307',       # the default MySQL port
    }
}"""


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = False
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.environ.get('EMAIL_ADDRESS_SENDER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
