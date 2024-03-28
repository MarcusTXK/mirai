from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now(datetime.UTC))
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now(datetime.UTC))
    updatedBy = db.Column(db.String(255))

class Chatlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now(datetime.UTC))
    sentBy = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
