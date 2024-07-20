import os
from datetime import datetime
import random
from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Message
from werkzeug.utils import secure_filename
from app import db, bcrypt, mail, app
from user.user_register import User

feedback_bp = Blueprint('feedback', __name__)
UPLOAD_FOLDER = 'uploads/feedback'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mkv', 'pdf', 'txt', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('feedback', lazy=True))

@feedback_bp.route('/submit_feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    if 'file' not in request.files or 'description' not in request.form:
        return jsonify({"error": "File and description are required"}), 400

    file = request.files['file']
    description = request.form['description']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        user_id = get_jwt_identity()
        feedback = Feedback(user_id=user_id, description=description, file_path=file_path)
        db.session.add(feedback)
        db.session.commit()

        return jsonify({"message": "Feedback submitted successfully"}), 201

    return jsonify({"error": "File type not allowed"}), 400

@feedback_bp.route('/admin/view_feedback', methods=['GET'])
@jwt_required()
def view_feedback():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    
    if not user or not user.is_admin:
        return jsonify({"error": "Access denied"}), 403

    feedback_list = Feedback.query.all()
    feedback_data = []
    for feedback in feedback_list:
        feedback_data.append({
            'id': feedback.id,
            'user_id': feedback.user_id,
            'username': feedback.user.username,
            'description': feedback.description,
            'file_path': feedback.file_path,
            'timestamp': feedback.timestamp
        })

    return jsonify(feedback_data), 200

@feedback_bp.route('/uploads/feedback/<filename>', methods=['GET'])
@jwt_required()
def uploaded_file(filename):
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    
    if not user or not user.is_admin:
        return jsonify({"error": "Access denied"}), 403

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app.register_blueprint(feedback_bp)

if __name__ == '__main__':
    db.create_all()  # Ensure the database tables are created
    app.run(debug=True)
