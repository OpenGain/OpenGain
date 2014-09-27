from decimal import Decimal
import os
from django.utils import timezone
from datetime import datetime
import platform

# ------------------------------------
# Название проекта
PROJECT_TITLE = 'OpenGain Engine'

#Домен
PROJECT_DOMAIN = 'localhost:8000'

#Админы (сисадмины) и менеджеры
ADMINS = (('Admin1', 'admin1@opengain.host'), ('Admin2', 'admin2@opengain.host'))
MANAGERS = ADMINS
#------------------------------------

#Если имя хоста отличается от домена, прописать руками
DEBUG = platform.node() != PROJECT_DOMAIN
TEMPLATE_DEBUG = DEBUG


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '%qlb42=*f_^pj50$u*=-2b=1r&yx8ubn()5p3e)9=ok36w1=p2'

SERVER_EMAIL = 'Робот OpenGain <robot@opengain.host>'

DEFAULT_FROM_EMAIL = SERVER_EMAIL

LOGIN_URL = '/user/signin/'

LOGOUT_URL = '/user/signout/'

AUTH_USER_MODEL = 'default_set.UserProfile'

INSTALLED_APPS = (
    #Сторонние
    'modeltranslation',  # ==0.8b2
    'rosetta',
    'bootstrap3',

    #Ядро
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    #Сторонние, патченные
    'captcha',

    #Базовые
    'main',
    'default_set',
    'default_set.reviews',
    'default_set.tickets',
    'default_set.news',
    'default_set.staticpages',
    'default_set.dialogs',

    #Платежки
    'payment_systems.perfect_money',
    'payment_systems.payeer',
    #'payment_systems.egopay',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'opengain.middlewares.ChangeUserLanguage',
    'opengain.middlewares.DeactivateUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'opengain.urls'

WSGI_APPLICATION = 'opengain.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'main.context_processors.settings_prosessor',
    'main.context_processors.protocol_processor',
    'main.context_processors.statistic_processor',
    'default_set.dialogs.context_processors.unread_dialogs_messages',
)

#sqlite3 не использовать! Она не поддерживает SELECT FOR UPDATE.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'opengain',
        'USER': 'opengain',
        'PASSWORD': 'dEzKXJdlG8SXmULM',
        'HOST': 'localhost',
    }
}

LANGUAGES = (
    ('ru', 'Русский'),
    ('en', 'English'),
)

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), '..', 'formats'),
)

LANGUAGE_CODE = 'ru'

MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

USE_THOUSAND_SEPARATOR = False

FORMAT_MODULE_PATH = 'main.formats'

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

if DEBUG:
    EMAIL_BACKEND = 'main.backends.email_backends.EmailBackend'
    EMAIL_FILE_PATH = 'tmp/eml/'

#------------------------------------Project settings

#На какие домены можно заходить
ALLOWED_HOSTS = [PROJECT_DOMAIN, 'www.' + PROJECT_DOMAIN]

#Куда перенаправлять юзера по реферальной ссылке
REFLINK_REDIRECT = 'account_signup'

#Дата старта проекта
PROJECT_START_DATETIME = datetime(2014, 7, 10, 12, 0, 0, 0).replace(tzinfo=timezone.get_default_timezone())

#Реферальные комиссии по уровням соответственно. Количество чисел и означает количество уровней.
REFERRAL_COMISSIONS = (25, 15, 10)

#Комиссия на вывод в процентах
WITHDRAW_COMISSION_PERCENT = 3

#Минимальный единовременный вывод
WITHDRAWAL_MIN = Decimal(1)

#Максимальный единовременный вывод
WITHDRAWAL_MAX = Decimal(9999)

#Минимальный единовременный ввод
DEPOSIT_MIN = Decimal(10)

#Максимальный единовременный ввод
DEPOSIT_MAX = Decimal(10000)

#URL админки (без слешей)
ADMIN_URL = 'adminka'

#URL админки переводчика (без слешей)
TRANSLATION_URL = 'trans'

#------------------------------------Perfect Money settings

PM_ACCOUNT = ''
PM_WALLET = ''
PM_PASSWORD = ''
PM_PASSPHRASE = ''

#------------------------------------Payeer settings

PAYEER_ACCOUNT = ''
PAYEER_SHOP_ID = ''
PAYEER_SHOP_KEY = ''
PAYEER_API_ID = ''
PAYEER_API_KEY = ''
PAYEER_RESULT_URL = 'result'
