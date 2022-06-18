import  os

class Config(object):
    DEBUG = False
    SECRET_KEY = 'estoesunsecreto'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    
class DevConfig(Config):
    DEBUG = True

