import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Prod(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////data/database.db'
    PROPAGATE_EXCEPTIONS = True
    MAGENTO_URL = os.getenv('MAGENTO_URL')
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
    AUTH_TOKEN = os.getenv('AUTH_TOKEN')
    WS_URL = os.getenv('WS_URL')
    DEFAULT_USERNAME = os.getenv('DEFAULT_USERNAME')
    DEFAULT_PASSWORD = os.getenv('DEFAULT_PASSWORD')
    DEFAULT_NAME = os.getenv('DEFAULT_NAME')
    DEFAULT_EMAIL = os.getenv('DEFAULT_EMAIL')

class Dev(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    PROPAGATE_EXCEPTIONS = True
    MAGENTO_URL = os.getenv('MAGENTO_URL')
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
    AUTH_TOKEN = os.getenv('AUTH_TOKEN')
    WS_URL = os.getenv('WS_URL')
    DEFAULT_USERNAME = os.getenv('DEFAULT_USERNAME')
    DEFAULT_PASSWORD = os.getenv('DEFAULT_PASSWORD')
    DEFAULT_NAME = os.getenv('DEFAULT_NAME')
    DEFAULT_EMAIL = os.getenv('DEFAULT_EMAIL')

class Test(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_TOKEN = 'test_apitoken_test_apitoken'
    DEFAULT_USERNAME = 'test_username'
    DEFAULT_PASSWORD = 'test_password'
    DEFAULT_NAME = 'test_name'
    DEFAULT_EMAIL = 'test_email@email.com'
