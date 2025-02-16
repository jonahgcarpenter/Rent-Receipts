from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash

from app import db
from app.models import Users

user_bp = Blueprint("users", __name__, url_prefix="/api/users")


@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    user_data = {
        "username": user.username,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "household_id": user.household_id,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }
    return jsonify(user_data), 200


@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    username = data.get("username")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    password = data.get("password")

    if username:
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"msg": "Username already exists"}), 400
        user.username = username

    if firstName:
        user.firstName = firstName

    if lastName:
        user.lastName = lastName

    if password:
        user.password = generate_password_hash(password)

    db.session.commit()
    return jsonify({"msg": "User updated successfully"}), 200


@user_bp.route("/profile", methods=["DELETE"])
@jwt_required()
def delete_profile():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"}), 200
