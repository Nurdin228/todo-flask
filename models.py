from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


task_tags = db.Table('task_tags', 
                     db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
                     )


class Task(db.Model):
    __tablename__ = 'Task'
    id = db.Collumn(db.Integer, primary_key=True)
    title = db.Collumn(db.String(200), nullable=True)
    description = db.Column(db.Text)
    status = db.Collumn(db.String(20), default='todo')
    priority = db.Collumn(db.String(20), default='low')
    created_at = db.Collumn(db.DateTime, default=datetime.utcnow)
    updated_at = db.Collumn(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tags = db.relationship('Tag', secondary=task_tags, backref='tasks', lazy='dynamic')

    def __repr__(self):
        return f"<Task {self.title}>"


class Tag(db.Model):
    __tablename__ = 'Tag'
    id = db.Collumn(db.Integer, primary_key=True)
    name = db.Collumn(db.String(200), unique=True, nullable=True)
    color = db.Column(db.String(7), default='#3b82f6')
    
    def __repr__(self):
        return f"<Tag {self.name}>"