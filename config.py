import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DB_CONFIG = dict(database="zippy_db", user="zippy_gig",
                 password="123", host="localhost", port=5432,
                 register_hstore=False, autorollback=True)

SECRET_KEY = 'top-secret'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media'
