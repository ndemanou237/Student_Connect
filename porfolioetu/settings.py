# portfolioetu/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv

# charge le fichier .env si on est en développement
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# SÉCURITÉ
# ============================================================
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'dev-key-change-this-in-production-please'
)

# DEBUG = False en production automatiquement
# Railway définit DEBUG=False dans ses variables d'environnement
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS — on accepte tous les sous-domaines railway.app
# et le domaine personnalisé si tu en as un
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost 127.0.0.1'
).split(' ')

# en production, Railway donne l'URL du site dans RAILWAY_PUBLIC_DOMAIN
RAILWAY_HOST = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
if RAILWAY_HOST:
    ALLOWED_HOSTS.append(RAILWAY_HOST)

# ============================================================
# APPLICATIONS
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'etudiants',
]

# ============================================================
# MIDDLEWARE
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # whitenoise en 2ème — sert les fichiers CSS/JS en production
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolioetu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'portfolioetu.wsgi.application'

# ============================================================
# BASE DE DONNÉES
# ============================================================
# Railway fournit automatiquement DATABASE_URL quand tu ajoutes PostgreSQL
# dj-database-url lit cette variable et configure Django automatiquement
import dj_database_url

# DATABASE_URL est définie automatiquement par Railway
# en développement on utilise notre .env
DATABASE_URL = os.environ.get('DATABASE_URL', '')

if DATABASE_URL:
    # production — Railway donne une URL complète comme :
    # postgresql://user:password@host:5432/dbname
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,      # garde les connexions ouvertes 10 min
            conn_health_checks=True # vérifie que la connexion est active
        )
    }
else:
    # développement local — on utilise nos variables séparées
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'portfolioetu_db'),
            'USER': os.environ.get('DB_USER', 'portfolioetu_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# ============================================================
# MOT DE PASSE
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================
# LANGUE ET TIMEZONE
# ============================================================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

# ============================================================
# FICHIERS STATIQUES
# ============================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# dossier où collectstatic copie tout en production
STATIC_ROOT = BASE_DIR / 'staticfiles'
# whitenoise compresse et met en cache les fichiers statiques
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================================
# FICHIERS MÉDIA
# ============================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# REDIRECTIONS AUTH
# ============================================================
LOGIN_REDIRECT_URL  = '/mon-espace/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL           = '/connexion/'

# ============================================================
# SÉCURITÉ PRODUCTION
# ============================================================
# ces paramètres s'activent seulement quand DEBUG=False
if not DEBUG:
    # force HTTPS
    SECURE_SSL_REDIRECT = True
    # indique au navigateur de toujours utiliser HTTPS
    SECURE_HSTS_SECONDS = 31536000       # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    # cookies sécurisés — envoyés seulement en HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE    = True
    # Railway utilise un proxy — on lui fait confiance
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'