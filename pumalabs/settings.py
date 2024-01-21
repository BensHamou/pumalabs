from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

AUTHENTICATION_BACKENDS = [
    'account.authentication.ApiBackend',
    'django.contrib.auth.backends.ModelBackend',
    ]

with open(os.path.join(BASE_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

DEBUG = True

AUTH_USER_MODEL = 'account.User'

swappable = 'AUTH_USER_MODEL'

ADMIN_URL = 'puma_labs/admin/'

ALLOWED_HOSTS = ['*']

CSRF_COOKIE_SECURE = False

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "account",
    "report",
    'bootstrap5',
    'fontawesomefree',
    'django_filters',
    'widget_tweaks',
    'django_extensions',
    'django_crontab'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pumalabs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'account', 'templates', 'user'), os.path.join(BASE_DIR, 'account', 'templates', 'usine'),
                 os.path.join(BASE_DIR, 'account', 'templates', 'horaire'), os.path.join(BASE_DIR, 'account', 'templates', 'fragment'),
                 os.path.join(BASE_DIR, 'report', 'templates', 'poste'), os.path.join(BASE_DIR, 'report', 'templates', 'report'), 
                 os.path.join(BASE_DIR, 'report', 'templates', 'modal'), os.path.join(BASE_DIR, 'report', 'templates', 'fournisseur')
                 ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pumalabs.wsgi.application"

DATABASES = {
    #default': {
    #   'ENGINE': 'django.db.backends.postgresql',
    #   'NAME': 'LabDBDev',
    #   'USER': 'puma_prod',
    #   'PASSWORD': 'puma_prod',
    #   'HOST': '10.10.10.101',
    #   'PORT': '5434',
    #
    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql',
    #    'NAME': 'PumaLab',
    #    'USER': 'lab_report',
    #    'PASSWORD': 'lab_report',
    #    'HOST': '10.10.10.53',
    #    'PORT': '5400',
    #}
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "fr"

TIME_ZONE = "Africa/Algiers"

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / "static"]

LOGIN_REDIRECT_URL = 'login_success'
LOGOUT_REDIRECT_URL = '/login'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'pumalabs001@gmail.com'
EMAIL_HOST_PASSWORD = 'bvliwpvyejfhfaln'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'pumalabs001@gmail.com'