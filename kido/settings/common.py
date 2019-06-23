from kido import app

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
WTF_CSRF_ENABLED = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
COMPRESSOR_DEBUG = True
COMPRESSOR_OUTPUT_DIR = app.static_folder + '/sdist'
COMPRESSOR_STATIC_PREFIX = app.static_url_path + '/sdist'
MAPBOX_MAP_ID = None


# Overwrite above settings with test data
# If we aren't on a test machine, the file shouldn't exist
try:
    from .test import *
except ImportError:
    pass


# Overwrite above settings with dev data
# If we aren't on a dev machine, the file shouldn't exist
try:
    from .development import *
except ImportError:
    pass


# Overwrite above settings with production data
# If we aren't on a prod machine, the file shouldn't exist
try:
    from .production import *
except ImportError:
    pass


auth = ''
if DB_USERNAME and DB_PASSWORD:
    auth = '{user}:{password}@'.format(user=DB_USERNAME, password=DB_PASSWORD)
SQLALCHEMY_DATABASE_URI = 'postgresql://{auth}{host}/{database}'.format(
    auth=auth,
    host=DB_HOST,
    database=DB_NAME,
)
