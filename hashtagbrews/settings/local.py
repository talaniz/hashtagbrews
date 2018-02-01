from .base import *

DEBUG = True

INSTALLED_APPS += ('debug_toolbar', 'django_info_panel', 'django_extensions',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hashtagbrews',
        'USER': 'hashtagbrews',
        'PASSWORD': '@ntonio1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
