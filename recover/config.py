import ConfigParser

from peewee import *


def read_configs(paths):
    config = ConfigParser.ConfigParser()
    configs_read = config.read(paths)
    if not configs_read:
        raise NoConfigError('No config file!')
    return config

config = read_configs('database.cfg')

try:
    SQLITE3_PATH = config.get('sqlite3', 'path')
except:
    SQLITE3_PATH = None

try:
    MYSQL_HOST = config.get('mysql', 'host')
    MYSQL_NAME = config.get('mysql', 'name')
    MYSQL_USER = config.get('mysql', 'user')
    MYSQL_PASS = config.get('mysql', 'pass')
except:
    MYSQL_HOST = None
    MYSQL_NAME = None
    MYSQL_USER = None
    MYSQL_PASS = None

if SQLITE3_PATH:
    db = SqliteDatabase(
        SQLITE3_PATH
    )
elif MYSQL_HOST and MYSQL_NAME and MYSQL_USER and MYSQL_PASS:
    db = MySQLDatabase(
        MYSQL_NAME,
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
    )

# SAMPLE database.cfg file::
# --------------------------------------
# [sqlite3]
# filename=
# 
# [mysql]
# host=
# name=
# user=
# pass=
# --------------------------------------
