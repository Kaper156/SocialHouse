"""
Django settings for SocialHouse project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# sys.path.append(os.path.join(BASE_DIR, 'applications/'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ujgzqxm)y)ea4l3i^n+k&c@(ex09chvb(3x8hyf+-0_3-(q77^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
ANOTHER_APPS_PRE = [
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
ANOTHER_APPS_POST = [
    'formtools',
    'slugify',
    'crispy_forms',
    'django_extensions',
]
MY_APPLICATIONS = [
    'applications.people',
    'applications.serviced_data',
    'applications.documents',

    'applications.social_work',
    'applications.social_work.ippsu',
    'applications.social_work.providing',
    'applications.social_work.limitations',
    'applications.social_work.services',
    'applications.social_work.acts',

    'applications.receptionist',
    'applications.receptionist.visits',
    'applications.receptionist.sleepover',
    'applications.receptionist.meter',
    'applications.receptionist.movements',

    'applications.website',
    'applications.website.news',
    'applications.website.cabinet',

]
INSTALLED_APPS = ANOTHER_APPS_PRE + INSTALLED_APPS
INSTALLED_APPS += ANOTHER_APPS_POST
INSTALLED_APPS += MY_APPLICATIONS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SocialHouse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.filesystem.Loader',

            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'SocialHouse.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

LOGIN_URL = "login/"
LOGOUT_URL = "logout/"
LOGIN_REDIRECT_URL = "/lk/profile/"

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Omsk'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # True

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DOCUMENTS_ROOT_FOLDER = os.path.abspath(os.path.join(MEDIA_ROOT, 'documents'))
MEDIA_URL = '/media/'

# STATICFILES_STORAGE = 'ManifestStaticFilesStorage'
# STATICFILES_DIRS += [f"/{app.replace('.', '/')}/static/" for app in MY_APPLICATIONS]

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'SocialHouse/fixtures')
]

GRAPH_MODELS = {
    'all_applications': False,
    'group_models': True,
    'exclude_models': 'Permission,ContentType,LogEntry,AbstractUser,User,Group',
    'output': './docs/models.png',
}

ADMIN_TOOLS_MENU = 'SocialHouse.at.menu.SocialHouseMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'SocialHouse.at.dashboard.SocialHouseIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'SocialHouse.at.dashboard.SocialHouseAppIndexDashboard'
