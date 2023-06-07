from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DJANGO_DB_NAME", "facilities"),
        'USER': os.environ.get("DJANGO_DB_USER", "facilities"),
        'PASSWORD': os.environ.get("DJANGO_DB_PASSWORD", "letmein"),
        'HOST': os.environ.get("DJANGO_DB_HOST", "localhost"),
        'PORT': os.environ.get("DJANGO_DB_PORT", "5432"),
    }
}

# Remove whitenoise from middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
