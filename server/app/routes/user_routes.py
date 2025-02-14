from app.services.user_service import get_all_users
from flask import Blueprint, jsonify

user_bp = Blueprint("user", __name__)


@user_bp.route("/", methods=["GET"])
def list_users():
    users = get_all_users()
    return jsonify(users)
