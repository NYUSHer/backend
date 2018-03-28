import pymysql
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    #SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    #FLASKY_MAIL_SENDER = 'Flasky Admin <flasky>@example.com'
    #FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
    threaded = True


class TestingConfig(Config):
    TESTING = True
    threaded = True


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = ''
    MAIL_SERVER = 'smtp.yeah.net'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'nyusher@yeah.net'
    MAIL_PASSWORD = os.environ['mailpwd']
    MAIL_DEBUG = False
    MAIL_USE_SSL = True
    threaded = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

VERBOSE = True

DOMAIN = 'nyusher.nya.vc'

PORT = 6680

PROTOCOL = 'https://'

# test
DB = {'host': 'nyusher.nya.vc', 'port':os.environ['DBport'],
                         'user':'root',
                         'password':os.environ['DBpwd'],
                         'db':'NYUSHer',
                         'charset': 'utf8',
                         'cursorclass': pymysql.cursors.DictCursor}

