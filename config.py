import os
class Config(object):
    DEBUG=False
    SECRET_KEY=os.environ.get('SECRET_KEY')

class ProductionConfig(Config):
    DEBUG=False

class DevelopmentConfig(Config):
    DEBUG=True
    REQ_USER=os.environ.get('REQ_USER')
    REQ_PASSWORD=os.environ.get('REQ_PASSWORD')