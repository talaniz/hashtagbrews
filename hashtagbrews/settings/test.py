from .base import *

DEBUG = True

SECRET_KEY = os.environ["SECRET_KEY"]

INSTALLED_APPS += ('debug_toolbar', 'django_info_panel', 'django_extensions',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hashtagbrews',
        'USER': 'hashtagbrews',
        'PASSWORD': os.environ["DB_PASSWORD"],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
