from app.services.user_service import create_new_user
from app.services.user_service import delete_user as service_delete_user
from app.services.user_service import get_all_users, get_user_by_id
from app.services.user_service import update_user as service_update_user
from flask import Blueprint, jsonify, request

user_bp = Blueprint("user", __name__)


@user_bp.route("/", methods=["GET"])
def list_users():
    users = get_all_users()
    return jsonify(users)


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Exclude the password field
    user_data = {"id": user.id, "username": user.username, "email": user.email}
    return jsonify(user_data)


@user_bp.route("/register", methods=["POST"])
def create_user():
    data = request.get_json()

    # Validate input
    if not data or not all(k in data for k in ["username", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400

    # Create the user
    success, message = create_new_user(
        data["username"], data["email"], data["password"]
    )

    if success:
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"error": message}), 400


@user_bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    success, message = service_update_user(user_id, data)
    if success:
        return jsonify({"message": message})
    else:
        return jsonify({"error": message}), 400


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success, message = service_delete_user(user_id)
    if success:
        return jsonify({"message": message})
    else:
        return jsonify({"error": message}), 400
