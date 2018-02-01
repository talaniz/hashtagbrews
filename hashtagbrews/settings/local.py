from .base import *

DEBUG = True

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
