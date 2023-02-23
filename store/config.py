from dotenv import load_dotenv
from os import environ, path

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    MYSQL_USER = environ.get('MYSQL_USER')
    MYSQL_PASS = environ.get('MYSQL_PASS')
    MYSQL_SERVER = environ.get('MYSQL_SERVER')
    MYSQL_DB = environ.get('MYSQL_DB')
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_SERVER}/{MYSQL_DB}'
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    IMAGE_DIR = environ.get('IMAGE_DIR')