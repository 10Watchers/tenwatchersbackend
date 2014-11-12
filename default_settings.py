import os
basedir = os.path.abspath(os.path.dirname(__file__))

API_KEY = ['foobar123']

HOST = '0.0.0.0'
PORT = 5000
DEBUG = True
TESTING = True

# Logging
ERROR_TO_FILE = True
ERROR_LOG_NAME = 'logs/errors.log'

ERROR_TO_EMAIL = False


URL_PREFIX_VERSION = '/api'


SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://tenwatcher:10watcher@tenwatcher.cqj6mu1ippgc.us-west-2.rds.amazonaws.com:5432/tenwatch'

DROP_TABLES=False

try:
    from local_settings import *
except ImportError:
    pass
