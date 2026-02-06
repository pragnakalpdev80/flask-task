from app.extensions import db

class User(db.Model):
    __tablename__ = 'registration_details'

    registration_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    hobbies=db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
