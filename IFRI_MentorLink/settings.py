from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-&g&mfc32i-q0kc4mpp9ih8$^eyz_vnb$6g_&+cr%l*roo3lwo-'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'gestion_comptes',
    'backend.gestion_comptes',
    'backend.messagerie',
    'backend.matching',
    'backend.offres_demandes',
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

ROOT_URLCONF = 'IFRI_MentorLink.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'IFRI_MentorLink.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ifri_mentorlink',
        'USER': 'postgres',
        'PASSWORD': 'ifri_mentorlink_2026',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'static',
]

ASGI_APPLICATION = 'IFRI_MentorLink.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

AUTH_USER_MODEL = 'gestion_comptes.User'

LOGIN_URL = 'connexion'
