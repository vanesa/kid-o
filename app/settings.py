import os

UPLOAD_FOLDER = 'static/images/photos/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
WTF_CSRF_ENABLED = False
IS_TRAVIS = os.environ.get('IS_TRAVIS') == 'true'
DB_NAME = 'kido' if not IS_TRAVIS else 'travis_ci_test'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/' + DB_NAME