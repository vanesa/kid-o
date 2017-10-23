import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
WTF_CSRF_ENABLED = False
IS_TRAVIS = os.environ.get('IS_TRAVIS') == 'true'
SQLALCHEMY_TRACK_MODIFICATIONS = False
COMPRESSOR_DEBUG = True

if os.environ.get('PRODUCTION'):
    from .production import *
else:
    from .development import *
