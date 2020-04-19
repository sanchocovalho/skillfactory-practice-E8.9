import enum
from sqlalchemy import Enum
from app import db

class Results(db.Model):
    __tablename__ = 'results'

    _id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(300), unique=False, nullable=True)
    word_count = db.Column(db.Integer, unique=False, nullable=True)
    elapsed_time = db.Column(db.Integer, unique=False, nullable=True)
    create_time = db.Column(db.DateTime())
    http_status_code = db.Column(db.Integer)
    status = db.Column(db.String(30))

class TaskStatus (enum.Enum):
    UNSTARTED = 1
    PENDING = 2
    FINISHED = 3

class Tasks(db.Model):
    __tablename__ = 'tasks'

    _id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(300), unique=False, nullable=True)
    create_time = db.Column(db.DateTime())
    task_status = db.Column(Enum(TaskStatus))
    http_status = db.Column(db.Integer)
