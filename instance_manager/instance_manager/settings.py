"""
Django settings for sign_manager project.

Generated by 'django-admin startproject' using Django 1.11.29.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import django
import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.path.exists(os.path.join(BASE_DIR, 'fabfile.py')):
    TEST = True
else:
    TEST = False


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c-y$7ru%mmmne@)7q+#6)ifqhn9vt%4fcll0_r&q7+m3%ez4ku'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'task',
    'account',
    'region_ec2_manager'
]

CRONJOBS = [
    ('*/30 * * * *', 'task.region_ec2_update.main', '>>{0}'.format(os.path.join(BASE_DIR, 'logs/instance_region.log')))
]

AUTHENTICATION_BACKENDS = ['account.backend.LoginModelBackend']

AUTH_USER_MODEL = 'account.UserAccount'

MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'instance_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.templatetags.static'
            ]
        },

    },
]

WSGI_APPLICATION = 'instance_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if TEST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'lbe_manager',
            'USER': 'django',
            'PASSWORD': 'Django.Password2020',
            'HOST': '127.0.0.1',
            'PORT': 14449,
            'OPTIONS': {
                'charset': 'utf8mb4',
            }
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'lbe_manager',
            'USER': 'django',
            'PASSWORD': 'Django.Password2020',
            'HOST': 'meet-ec2-manager.cvmkr4lnjp0j.ap-southeast-1.rds.amazonaws.com',
            'PORT': 3306,
            'OPTIONS': {
                'charset': 'utf8mb4',
            }
        },
    }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # ('img', os.path.join(STATIC_ROOT, 'img')),
    ('css', os.path.join(STATIC_ROOT, 'css')),
    ('js', os.path.join(STATIC_ROOT, 'js')),
    ('AdminLTE/bootstrap', os.path.join(STATIC_ROOT, 'AdminLTE/bootstrap')),
    ('AdminLTE/dist', os.path.join(STATIC_ROOT, 'AdminLTE/dist')),
    ('AdminLTE/plugins', os.path.join(STATIC_ROOT, 'AdminLTE/plugins')),
    ('highcharts', os.path.join(STATIC_ROOT, 'highcharts')),
    ('vue/js', os.path.join(STATIC_ROOT, 'vue/js')),
    ('vue/elementui', os.path.join(STATIC_ROOT, 'vue/elementui')),
    ('vue/css', os.path.join(STATIC_ROOT, 'vue/css')),
    ('bootstrap', os.path.join(STATIC_ROOT, 'bootstrap-3.3.7'))
]

CSRF_COOKIE_AGE = 2 * 3600
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_FAILURE_VIEW = 'account.util.csrf_failure'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)-8s %(message)s'
        },
        'detail': {
            'format': '%(thread)d %(asctime)s %(levelname)-8s %(pathname)s %(funcName)s  [line:%(lineno)d] %(message)s'
        },
    },
    'handlers': {
        'root_handler': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/root.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 100,
            'formatter': 'detail',
        },
        'django_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 100,
            'formatter': 'detail',
        },
        'anchor_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 100,
            'formatter': 'detail',
        },
    },
    'loggers': {
        'info': {
            'handlers': ['django_handler'],
            'level': 'INFO',
            'propagate': True,
        },
        'root': {
            'handlers': ['root_handler'],
            'level': 'WARNING',
            'propagate': True,
        },
        'anchor': {
            'handlers': ['anchor_handler'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
django.setup()