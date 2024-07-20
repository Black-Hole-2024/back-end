import os
import random
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
import secrets  # For generating secure tokens

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), '..', 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'masri12345'
app.config['JWT_SECRET_KEY'] = 'masri12345'

# Email configuration (use your own SMTP server details)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'masrialemu@gmail.com'
app.config['MAIL_PASSWORD'] = 'mwxb ixae valq szin'  # Make sure to handle sensitive data securely
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6))  # For email verification
    reset_token = db.Column(db.String(6))  # For password reset (6-digit code)
    reset_token_expiration = db.Column(db.DateTime)  # Expiration time of the reset token

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    fullname = data.get('fullname')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not fullname or not username or not email or not password or not confirm_password:
        return jsonify({"error": "All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"error": "Username already exists"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"error": "Email already exists"}), 400

    verification_code = str(random.randint(100000, 999999))  # Ensure the code is a string
    new_user = User(fullname=fullname, username=username, email=email, password=hashed_password, verification_code=verification_code)
    db.session.add(new_user)
    db.session.commit()

    # Create HTML content for the email
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f2f2f2;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #333333;">Welcome to Our Service!</h2>
            <p style="font-size: 16px; color: #555555;">Hi {fullname},</p>
            <p style="font-size: 16px; color: #555555;">Thank you for signing up! To complete your registration, please use the following verification code:</p>
            <h3 style="font-size: 24px; color: #007bff;">{verification_code}</h3>
            <p style="font-size: 16px; color: #555555;">If you did not create an account, please ignore this email.</p>
            <p style="font-size: 16px; color: #555555;">Best regards,</p>
            <p style="font-size: 16px; color: #555555;">The Team</p>
        </div>
    </body>
    </html>
    """

    msg = Message('Verify Your Email', sender='your_email@example.com', recipients=[email])
    msg.html = html
    try:
        mail.send(msg)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "User registered successfully. Check your email for the verification code.", "verification_code": verification_code}), 201

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    username = data.get('username')
    verification_code = data.get('verification_code')

    user = User.query.filter_by(username=username).first()

    if user and user.verification_code == verification_code:  # Check against stored verification code
        user.is_active = True
        user.verification_code = None  # Clear the verification code once verified
        db.session.commit()
        return jsonify({"message": "User verified successfully"}), 200

    return jsonify({"error": "Invalid verification code or username"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    if user.is_blocked:
        return jsonify({"error": "User is blocked"}), 403

    if not user.is_active:
        return jsonify({"error": "User is not verified"}), 403

    access_token = create_access_token(identity={'username': user.username, 'is_admin': user.is_admin})
    return jsonify(access_token=access_token), 200

@app.route('/block_user', methods=['POST'])
@jwt_required()
def block_user():
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({"error": "Admin access required"}), 403

    data = request.json
    username = data.get('username')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_blocked = True
    db.session.commit()
    return jsonify({"message": "User blocked successfully"}), 200

@app.route('/users', methods=['GET'])
@jwt_required()  # Ensure the user is authenticated to access this endpoint
def get_users():
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({"error": "Admin access required"}), 403

    users = User.query.all()
    user_list = [{
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin,
        "is_active": user.is_active,
        "is_blocked": user.is_blocked
    } for user in users]

    return jsonify(user_list), 200





@app.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    data = request.json
    email = data.get('email')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Email not found"}), 404

    # Generate a 6-digit reset code
    reset_code = str(random.randint(100000, 999999))
    reset_token_expiration = datetime.utcnow() + timedelta(minutes=15)  # Code valid for 15 minutes

    user.reset_token = reset_code
    user.reset_token_expiration = reset_token_expiration
    db.session.commit()

    # Create HTML content for the email
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f2f2f2;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #333333;">Password Reset Request</h2>
            <p style="font-size: 16px; color: #555555;">Hi {user.fullname},</p>
            <p style="font-size: 16px; color: #555555;">We received a request to reset your password. Use the following code to reset your password:</p>
            <h3 style="font-size: 24px; color: #007bff;">{reset_code}</h3>
            <p style="font-size: 16px; color: #555555;">This code is valid for 15 minutes. If you did not request a password reset, please ignore this email.</p>
            <p style="font-size: 16px; color: #555555;">Best regards,</p>
            <p style="font-size: 16px; color: #555555;">The Team</p>
        </div>
    </body>
    </html>
    """

    msg = Message('Password Reset Request', sender='Masri404', recipients=[email])
    msg.html = html
    try:
        mail.send(msg)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Password reset email sent"}), 200

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    reset_code = data.get('reset_code')  # Updated to reset_code
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')

    if new_password != confirm_new_password:
        return jsonify({"error": "Passwords do not match"}), 400

    user = User.query.filter_by(reset_token=reset_code).first()  # Updated to reset_code

    if not user or user.reset_token_expiration < datetime.utcnow():
        return jsonify({"error": "Invalid or expired reset code"}), 400

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    user.password = hashed_password
    user.reset_token = None
    user.reset_token_expiration = None
    db.session.commit()

    return jsonify({"message": "Password reset successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
