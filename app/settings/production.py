import os

DB_HOST = os.environ.get('DB_HOST')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

COMPRESSOR_DEBUG = False
COMPRESSOR_OFFLINE_COMPRESS = True