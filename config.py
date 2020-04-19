import os

class Config():
    DEBUG = False
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_BACKEND')
    NSQTCP_ADDRESS = os.getenv('NSQTCP_ADDRESS')
    NSQHTTP_ADDRESS = os.getenv('NSQHTTP_ADDRESS')
    NSQ_TOPIC = os.getenv('NSQ_TOPIC')
    NSQ_CHANNEL=os.getenv('NSQ_CHANNEL')