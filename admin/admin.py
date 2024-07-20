from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/block_user', methods=['POST'])
@jwt_required()
def block_user():
    from app import db  # Import here to avoid circular import
    from user.models import User  # Import here to avoid circular import

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

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    from app import db  # Import here to avoid circular import
    from user.models import User  # Import here to avoid circular import

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
