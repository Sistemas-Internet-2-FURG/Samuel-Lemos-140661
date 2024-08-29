from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CarType(db.Model):
    __tablename__ = 'car_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cars = db.relationship('Car', backref='car_type', lazy=True)

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))
    type_id = db.Column(db.Integer, db.ForeignKey('car_types.id'), nullable=False)
