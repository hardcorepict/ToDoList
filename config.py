import os

basedir = os.path.abspath(os.path.dirname(__name__))

class Config():

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Fhsd4asGko2asd2aDdk'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #Email settings
    """
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    """
    ADMINS = ['murreyandy89@gmail.com']
    
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME='murreyandy89@gmail.com'
    MAIL_PASSWORD='a1coho1e'