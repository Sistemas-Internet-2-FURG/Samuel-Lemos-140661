from app.config.db import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user = db.relationship('User', back_populates='courses')

    def __repr__(self):
        return f'<Course {self.name}>'
    