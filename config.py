"""
Configuration for the flask app.
"""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(basedir, '.env'), verbose=True)

class Config():
    """
    Contains all the configurations for the project.
    """
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    ADMINS = ['khokhlov.ivan@yahoo.com']

    POSTS_PER_PAGE = 10
    LANGUAGES = ['en', 'es']
    
    MS_TRANSLATOR_KEY = os.getenv('MS_TRANSLATOR_KEY')
    