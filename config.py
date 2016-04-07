import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "secret"
TEST_PATH = os.path.join(basedir, "Tests")
TEST_RESULT_PATH = os.path.join(basedir, "TestResults")
TOKEN_EXPIRATION_TIME = 99999
DEBUG = True