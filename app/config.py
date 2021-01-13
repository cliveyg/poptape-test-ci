# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    # set app configs
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CHECK_ACCESS_URL = os.getenv('CHECK_ACCESS_URL')
    ADDRESS_LIMIT_PER_PAGE = os.getenv('ADDRESS_LIMIT_PER_PAGE')
    LOG_FILENAME = os.getenv('LOG_FILENAME')
    LOG_LEVEL = os.getenv('LOG_LEVEL')

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_TESTDB_URI')
    ADDRESS_LIMIT_PER_PAGE = "2"
    LOG_LEVEL = "DEBUG"
