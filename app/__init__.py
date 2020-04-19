from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

@app.template_filter('datetime')
def format_datetime(value, format="%d-%m-%Y %H:%M:%S"):
    if value is None:
        return ""
    return value.strftime(format)

from app import routes, models, forms
db.create_all()
