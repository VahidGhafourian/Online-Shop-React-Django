from .settings import *
SECRET_KEY = config('django-insecure-iw1xh*s(69_$p@=3lbb4$3g)q##!ojx=334ezizovjz2n*^s38m')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
