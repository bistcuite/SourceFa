from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-nazd-*vy(2)8m@+@lt4(k5!!r!c311f=o1*fss6p&i9^%zmo&c'

DEBUG = True

ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'user.CustomUser'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'markdownify.apps.MarkdownifyConfig',

    'core',
    'user',
    'utils',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sourcefa.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'sourcefa.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'core/static'),
    os.path.join(BASE_DIR,'repos/'),
    os.path.join(BASE_DIR,'zips/'),
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REPO_ROOT = os.path.join(BASE_DIR,'repos','repos')
REPO_URL = '/repo/'

ZIP_ROOT = os.path.join(BASE_DIR,'zips','zips')
ZIP_URL = '/zips/'

MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            'div',
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
            'a',
            'abbr',
            'acronym',
            'b',
            'blockquote',
            'em',
            'i',
            'li',
            'ol',
            'p',
            'strong',
            'ul',
            'img',
            'code',
            'pre',
            'table',
            'tr',
            'td',
        ],
        "WHITELIST_ATTRS": [
            'href',
            'src',
            'alt',
            'align',
        ],
        "LINKIFY_TEXT": {
            "PARSE_URLS": True,

            # Next key/value-pairs only have effect if "PARSE_URLS" is True
            "PARSE_EMAIL": True,
            "CALLBACKS": [],
            "SKIP_TAGS": [],
        },
        "SKIP_TAGS": [
            'script',
        ]
    }
}