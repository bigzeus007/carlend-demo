"""
Django settings for CarLend Demo.
"""

from pathlib import Path
import os
import dj_database_url
from environ import Env

# Initialisation des variables d'environnement
env = Env()
Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, ".env"))

# Répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent



# Détection du mode (LOCAL ou PRODUCTION)
ENVIRONMENT = env('ENVIRONMENT', default='production')

ROOT_URLCONF = 'carlend.urls'

# Configuration des bases de données
if ENVIRONMENT == 'local':
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),  # Mets ton mot de passe ici
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}
else:
    DATABASES = {
        'default': dj_database_url.config(default=env("DATABASE_URL"), conn_max_age=600, ssl_require=True)
    }



# Clé secrète Django (ne jamais laisser en dur en production)
SECRET_KEY = env('DJANGO_SECRET_KEY', default="default-unsafe-secret-key")

# Mode Debug (désactivé par défaut en production)
# DEBUG = env.bool("DEBUG", default=False)
DEBUG = True

# Hôtes autorisés (Railway + localhost)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["web-production-f848.up.railway.app", "127.0.0.1", "localhost"])

# Origines de confiance pour CSRF
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[
    "https://web-production-f848.up.railway.app",
    "http://127.0.0.1:8000",
])

# Configuration PostgreSQL (Railway)
# DATABASES = {
#     'default': dj_database_url.config(default=env("DATABASE_URL"))
# }

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    'whitenoise.runserver_nostatic',
    # Applications personnalisées
    'vehicles',
    'reservations',
    'historiques',
    'home',
    'parc',
    'users',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configuration des fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Gestion des fichiers médias
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# TEMPLATES
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "carlend.wsgi.application"

# Authentification utilisateur personnalisé
AUTH_USER_MODEL = 'users.User'

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Paramètres de session
SESSION_COOKIE_AGE = 3600  # 1 heure
SESSION_SAVE_EVERY_REQUEST = True

# Configuration du logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
}

# Redirections après connexion/déconnexion
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
