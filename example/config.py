import os
import configparser

APP_ENV = os.environ.get('APP_ENV') or 'local'  # or 'live' to load live
INI_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../conf/{}.ini'.format(APP_ENV))

CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)

POSTGRES = CONFIG['postgres']
DB_CONFIG = (POSTGRES['user'], POSTGRES['password'], POSTGRES['host'], POSTGRES['database'])
DATABASE_URL = "postgresql://%s:%s@%s/%s" % DB_CONFIG
# postgresql://postgres:1234@localhost:5432/postgres

DB_ECHO = True if CONFIG['database']['echo'] == 'yes' else False
DB_AUTOCOMMIT = True
LOG_LEVEL = CONFIG['logging']['level']
