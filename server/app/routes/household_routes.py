from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models import Households, Users

household_bp = Blueprint("households", __name__, url_prefix="/api/households")


@household_bp.route("/", methods=["POST"])
@jwt_required()
def create_household():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"msg": "Household name is required"}), 400

    new_household = Households(name=name, owner_id=current_user_id)
    db.session.add(new_household)
    db.session.commit()

    user.household_id = new_household.id
    db.session.commit()

    return (
        jsonify(
            {"msg": "Household created successfully", "household_id": new_household.id}
        ),
        201,
    )


@household_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_household():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)

    if not user or not user.household_id:
        return jsonify({"msg": "User is not in a household"}), 404

    household = Households.query.get(user.household_id)
    if not household:
        return jsonify({"msg": "Household not found"}), 404

    household_data = {
        "id": household.id,
        "name": household.name,
        "owner_id": household.owner_id,
        "created_at": household.created_at,
        "updated_at": household.updated_at,
    }
    return jsonify(household_data), 200


@household_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_household():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)

    if not user or not user.household_id:
        return jsonify({"msg": "User is not in a household"}), 404

    household = Households.query.get(user.household_id)
    if not household:
        return jsonify({"msg": "Household not found"}), 404

    if household.owner_id != current_user_id:
        return (
            jsonify({"msg": "Only the household owner can update the household"}),
            403,
        )

    data = request.get_json()
    new_name = data.get("name")

    if not new_name:
        return jsonify({"msg": "Household name is required"}), 400

    household.name = new_name
    db.session.commit()

    return jsonify({"msg": "Household name updated successfully"}), 200


@household_bp.route("/profile", methods=["DELETE"])
@jwt_required()
def delete_household():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)

    if not user or not user.household_id:
        return jsonify({"msg": "User is not in a household"}), 404

    household = Households.query.get(user.household_id)
    if not household:
        return jsonify({"msg": "Household not found"}), 404

    if household.owner_id != current_user_id:
        return (
            jsonify({"msg": "Only the household owner can delete the household"}),
            403,
        )

    Users.query.filter_by(household_id=household.id).update({"household_id": None})

    db.session.delete(household)
    db.session.commit()

    return jsonify({"msg": "Household deleted successfully"}), 200


@household_bp.route("/invite", methods=["POST"])
@jwt_required()
def invite_user():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)

    if not user or not user.household_id:
        return jsonify({"msg": "User is not in a household"}), 404

    household = Households.query.get(user.household_id)
    if household.owner_id != current_user_id:
        return jsonify({"msg": "Only the household owner can invite users"}), 403

    data = request.get_json()
    invitee_id = data.get("user_id")
    invitee = Users.query.get(invitee_id)

    if not invitee:
        return jsonify({"msg": "User not found"}), 404

    if invitee.household_id:
        return jsonify({"msg": "User is already in a household"}), 400

    invitee.household_id = household.id
    db.session.commit()

    return jsonify({"msg": "User invited successfully"}), 200


@household_bp.route("/leave", methods=["POST"])
@jwt_required()
def leave_household():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not user.household_id:
        return jsonify({"msg": "User is not part of any household"}), 400

    household = Households.query.get(user.household_id)
    if household and household.owner_id == current_user_id:
        return (
            jsonify(
                {"msg": "Household owner cannot leave. Delete the household instead."}
            ),
            403,
        )

    user.household_id = None
    db.session.commit()

    return jsonify({"msg": "User left the household successfully"}), 200
