__author__ = 'Girish'

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'Top SECRET'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:sharingan1@localhost/g2'
    RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
    #UPLOAD_FOLDER = os.path.join(basedir, 'app/static/upload')


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig
}
