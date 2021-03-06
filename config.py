"""
Configuration for the flask app.
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    '''
    Contains all the configurations for the project.
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.mail.yahoo.com' # os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587 # int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = True # os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USE_SSL = True # os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['khokhlov.ivan@yahoo.com']

    POSTS_PER_PAGE = 10
    LANGUAGES = ['en', 'es']
    