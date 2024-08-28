from app.config.db import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    addresses = db.relationship('Address', back_populates='cliente')

    def __repr__(self):
        return f'<Client {self.name}>'
    