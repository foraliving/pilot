import os

# from . import middleware

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jifprlo(jdra72-=48gbsq59=l)-4pjq09fwm0#xrtkrbcy5+o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'bootstrap_admin',
    'foraliving',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "account",
    'pinax_theme_bootstrap',
    'bootstrapform',
    'metron',
    'sslserver',
    'mail_templated',
    'bootstrap3',
    'categories',
    'categories.editor',
    # 'mptt',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",

    # "LoginRequiredMiddleware"

]

SITE_ID = 1
SITE_NAME = 'For a Living'

ROOT_URLCONF = 'foraliving_project.urls'
LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/foraliving/'
LOGIN_EXEMPT = ()

ALLOWED_HOSTS = ['falpilot2017.us-east-1.elasticbeanstalk.com', 'localhost', '127.0.0.1', '192.168.1.34']
AWS_ACCESS_KEY_ID = "AKIAJRR7IFMZEMQSE4Z"
AWS_SECRET_ACCESS_KEY = "2EFIVYrFO7jUJAs8mt0x3RYK7cnOiLfPA2duiW59"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'pinax_theme_bootstrap/templates/'
            # 'pinax_theme_bootstrap/templates/account'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "account.context_processors.account",
                # 'django.core.context_processors.request',
                'pinax_theme_bootstrap.context_processors.theme',
            ],
        },
    },
]

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

WSGI_APPLICATION = 'foraliving_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# Uncomment to go back to using sqlite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'iotd',
            'USER': 'iotd',
            'PASSWORD': 'iotd',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_ROOT = STATIC_ROOT = os.path.join(BASE_DIR, "..", "foraliving", "static")
STATIC_URL = '/static/'
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = PROJECT_PATH + '/media'
MEDIA_URL = '/media/'

EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_API_KEY = "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"
