from app.config.db import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    courses = db.relationship('Course', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.name}>'
    