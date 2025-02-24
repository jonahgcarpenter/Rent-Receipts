from app import db
from app.models import Users
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    firstName = data.get("firstName")
    lastName = data.get("lastName")

    if not username or not password or not firstName or not lastName:
        return (
            jsonify({"msg": "Missing username, password, firstName, or lastName"}),
            400,
        )

    if Users.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = Users(
        username=username,
        password=hashed_password,
        firstName=firstName,
        lastName=lastName,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = Users.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"msg": "User logged out successfully"}), 200
