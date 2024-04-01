from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, onupdate=datetime.utcnow)
    updatedBy = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None,
            'updatedBy': self.updatedBy,
        }

class Chatlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    sentBy = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'time': self.time.isoformat() if self.time else None,
            'sentBy': self.sentBy,
            'message': self.message,
        }

class IoTData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    data = db.Column(db.JSON, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'unit': self.unit,
            'location': self.location,
            'data': self.data,
            'time': self.time.isoformat() if self.time else None,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None,
        }