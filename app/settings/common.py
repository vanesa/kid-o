import os

UPLOAD_FOLDER = 'static/images/photos/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
WTF_CSRF_ENABLED = False
IS_TRAVIS = os.environ.get('IS_TRAVIS') == 'true'
DB_HOST = 'localhost'
DB_NAME = 'kido'
DB_USERNAME = None
DB_PASSWORD = None
SQLALCHEMY_TRACK_MODIFICATIONS = False
COMPRESSOR_DEBUG = True


# Overwrite above settings with production data
# If we aren't on a prod machine, the file shouldn't exist
try:
    from settings.production import *
except ImportError:
    pass


# Overwrite above settings with dev data
# If we aren't on a dev machine, the file shouldn't exist
try:
    from settings.development import *
except ImportError:
    pass


auth = ''
if DB_USERNAME and DB_PASSWORD:
	auth = '{user}:{password}@'.format(user=username, password=password)
SQLALCHEMY_DATABASE_URI = 'postgresql://{auth}{host}/{database}'.format(
	auth=auth,
    host=DB_HOST,
    database=DB_NAME,
)
