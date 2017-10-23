
DB_HOST = 'localhost'
DB_NAME = 'kido'
DB_USERNAME = 'kido'
DB_PASSWORD = 'kido'

auth = ''
if DB_USERNAME and DB_PASSWORD:
	auth = '{user}:{password}@'.format(user=DB_USERNAME, password=DB_PASSWORD)
SQLALCHEMY_DATABASE_URI = 'postgresql://{auth}{host}/{database}'.format(
	auth=auth,
    host=DB_HOST,
    database=DB_NAME,
)