from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)
    reset_token = db.Column(db.String(6), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)
