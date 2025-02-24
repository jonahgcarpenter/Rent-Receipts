from app import db
from app.models import (
    Households,
    Payments,
    ReceiptItems,
    Receipts,
    ReceiptShares,
    Users,
)
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

receipt_bp = Blueprint("receipts", __name__, url_prefix="/api/receipts")


@receipt_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_receipts():
    current_user_id = int(get_jwt_identity())
    user = Users.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    household = user.household
    if not household:
        return jsonify({"msg": "User is not in a household"}), 400

    receipts = Receipts.query.filter_by(household_id=household.id).all()

    all_receipts = []
    for receipt in receipts:
        receipt_data = {
            "id": receipt.id,
            "household_id": receipt.household_id,
            "total_cost": str(receipt.total_cost),
            "due_date": receipt.due_date.isoformat(),
            "created_at": receipt.created_at.isoformat(),
            "updated_at": receipt.updated_at.isoformat(),
            "items": [
                {
                    "id": item.id,
                    "expense_name": item.expense_name,
                    "expense_cost": str(item.expense_cost),
                    "payer_id": item.payer_id,
                    "created_at": item.created_at.isoformat(),
                }
                for item in receipt.items
            ],
            "shares": [
                {
                    "id": share.id,
                    "user_id": share.user_id,
                    "share": str(share.share),
                    "paid": str(share.paid),
                    "created_at": share.created_at.isoformat(),
                    "updated_at": share.updated_at.isoformat(),
                }
                for share in receipt.shares
            ],
            "payments": [
                {
                    "id": payment.id,
                    "user_id": payment.user_id,
                    "amount": str(payment.amount),
                    "payment_date": payment.payment_date.isoformat(),
                }
                for payment in receipt.payments
            ],
        }
        all_receipts.append(receipt_data)

    return jsonify(all_receipts), 200


@receipt_bp.route("/<int:receipt_id>", methods=["GET"])
@jwt_required()
def get_receipt_by_id(receipt_id):
    current_user_id = int(get_jwt_identity())
    user = Users.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    household = user.household
    if not household:
        return jsonify({"msg": "User is not in a household"}), 400

    receipt = Receipts.query.filter_by(id=receipt_id, household_id=household.id).first()
    if not receipt:
        return jsonify({"msg": "Receipt not found"}), 404

    receipt_data = {
        "id": receipt.id,
        "household_id": receipt.household_id,
        "total_cost": str(receipt.total_cost),
        "due_date": receipt.due_date.isoformat(),
        "created_at": receipt.created_at.isoformat(),
        "updated_at": receipt.updated_at.isoformat(),
        "items": [
            {
                "id": item.id,
                "expense_name": item.expense_name,
                "expense_cost": str(item.expense_cost),
                "payer_id": item.payer_id,
                "created_at": item.created_at.isoformat(),
            }
            for item in receipt.items
        ],
        "shares": [
            {
                "id": share.id,
                "user_id": share.user_id,
                "share": str(share.share),
                "paid": str(share.paid),
                "created_at": share.created_at.isoformat(),
                "updated_at": share.updated_at.isoformat(),
            }
            for share in receipt.shares
        ],
        "payments": [
            {
                "id": payment.id,
                "user_id": payment.user_id,
                "amount": str(payment.amount),
                "payment_date": payment.payment_date.isoformat(),
            }
            for payment in receipt.payments
        ],
    }

    return jsonify(receipt_data), 200


@receipt_bp.route("/", methods=["POST"])
@jwt_required()
def create_receipt():
    current_user_id = int(get_jwt_identity())
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

    data = request.get_json()
    due_date = data.get("due_date")
    items_data = data.get("items")

    if not due_date or not items_data:
        return jsonify({"msg": "Missing required fields: due_date and items"}), 400

    total_cost = 0
    for item in items_data:
        expense_cost = item.get("expense_cost")
        if not expense_cost:
            return (
                jsonify({"msg": "Each receipt item must include an expense_cost"}),
                400,
            )
        total_cost += float(expense_cost)

    receipt = Receipts(
        household_id=household.id,
        total_cost=total_cost,
        due_date=due_date,
    )
    db.session.add(receipt)
    db.session.flush()

    for item in items_data:
        receipt_item = ReceiptItems(
            receipt_id=receipt.id,
            expense_name=item.get("expense_name"),
            expense_cost=item.get("expense_cost"),
        )
        db.session.add(receipt_item)

    household_members = household.users
    num_members = len(household_members)

    share_amount = float(total_cost) / num_members
    for member in household_members:
        receipt_share = ReceiptShares(
            receipt_id=receipt.id,
            user_id=member.id,
            share=share_amount,
        )
        db.session.add(receipt_share)

    db.session.commit()
    return jsonify({"msg": "Receipt created", "receipt_id": receipt.id}), 201


@receipt_bp.route("/<int:receipt_id>", methods=["PUT"])
@jwt_required()
def update_receipt_items(receipt_id):
    current_user_id = int(get_jwt_identity())
    user = Users.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    household = user.household
    if not household:
        return jsonify({"msg": "User is not in a household"}), 400

    receipt = Receipts.query.filter_by(id=receipt_id, household_id=household.id).first()
    if not receipt:
        return jsonify({"msg": "Receipt not found"}), 404

    if household.owner_id != current_user_id:
        return (
            jsonify({"msg": "Only the household owner can update receipt items"}),
            403,
        )

    data = request.get_json()
    new_items = data.get("new_items", [])
    updated_items = data.get("updated_items", [])
    deleted_item_ids = data.get("deleted_item_ids", [])

    for item_id in deleted_item_ids:
        receipt_item = ReceiptItems.query.filter_by(
            id=item_id, receipt_id=receipt.id
        ).first()
        if receipt_item:
            db.session.delete(receipt_item)

    for item in updated_items:
        item_id = item.get("id")
        if not item_id:
            continue
        receipt_item = ReceiptItems.query.filter_by(
            id=item_id, receipt_id=receipt.id
        ).first()
        if receipt_item:
            if "expense_name" in item:
                receipt_item.expense_name = item["expense_name"]
            if "expense_cost" in item:
                receipt_item.expense_cost = item["expense_cost"]

    for item in new_items:
        expense_name = item.get("expense_name")
        expense_cost = item.get("expense_cost")
        if expense_name is None or expense_cost is None:
            continue
        new_item = ReceiptItems(
            receipt_id=receipt.id,
            expense_name=expense_name,
            expense_cost=expense_cost,
        )
        db.session.add(new_item)

    db.session.flush()

    total_cost = sum(float(item.expense_cost) for item in receipt.items)
    receipt.total_cost = total_cost

    household_members = household.users
    num_members = len(household_members)
    if num_members == 0:
        return jsonify({"msg": "Household has no members"}), 400

    new_share = total_cost / num_members
    for share in receipt.shares:
        share.share = new_share

    db.session.commit()
    return (
        jsonify(
            {"msg": "Receipt items updated successfully", "receipt_id": receipt.id}
        ),
        200,
    )


@receipt_bp.route("/<int:receipt_id>/payments", methods=["PUT"])
@jwt_required()
def update_payment(receipt_id):
    current_user_id = int(get_jwt_identity())
    user = Users.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not user.household:
        return jsonify({"msg": "User is not in a household"}), 400

    receipt = Receipts.query.filter_by(
        id=receipt_id, household_id=user.household.id
    ).first()
    if not receipt:
        return jsonify({"msg": "Receipt not found"}), 404

    data = request.get_json()
    item_id = data.get("item_id")
    payment_amount = data.get("payment_amount")

    if (item_id is None and payment_amount is None) or (
        item_id is not None and payment_amount is not None
    ):
        return (
            jsonify(
                {"msg": "Provide either 'item_id' or 'payment_amount', but not both"}
            ),
            400,
        )

    receipt_share = next(
        (share for share in receipt.shares if share.user_id == current_user_id), None
    )
    if not receipt_share:
        return jsonify({"msg": "Receipt share for user not found"}), 404

    if item_id is not None:
        receipt_item = ReceiptItems.query.filter_by(
            id=item_id, receipt_id=receipt.id
        ).first()
        if not receipt_item:
            return jsonify({"msg": "Receipt item not found"}), 404
        try:
            amount_to_pay = float(receipt_item.expense_cost)
        except (ValueError, TypeError):
            return jsonify({"msg": "Invalid expense cost on the receipt item"}), 400

        receipt_item.payer_id = current_user_id
    else:
        try:
            amount_to_pay = float(payment_amount)
        except (ValueError, TypeError):
            return jsonify({"msg": "Invalid payment amount"}), 400

    new_payment = Payments(
        receipt_id=receipt.id, user_id=current_user_id, amount=amount_to_pay
    )
    db.session.add(new_payment)

    receipt_share.paid = float(receipt_share.paid) + amount_to_pay

    db.session.commit()
    return (
        jsonify({"msg": "Payment updated successfully", "paid": receipt_share.paid}),
        200,
    )


@receipt_bp.route("/<int:receipt_id>/payments/<int:payment_id>", methods=["DELETE"])
@jwt_required()
def delete_payment(receipt_id, payment_id):
    current_user_id = int(get_jwt_identity())
    user = Users.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not user.household:
        return jsonify({"msg": "User is not in a household"}), 400

    receipt = Receipts.query.filter_by(
        id=receipt_id, household_id=user.household.id
    ).first()
    if not receipt:
        return jsonify({"msg": "Receipt not found"}), 404

    payment = Payments.query.filter_by(id=payment_id, receipt_id=receipt.id).first()
    if not payment:
        return jsonify({"msg": "Payment not found"}), 404

    if payment.user_id != current_user_id:
        return jsonify({"msg": "You are not authorized to delete this payment"}), 403

    receipt_share = next(
        (share for share in receipt.shares if share.user_id == current_user_id), None
    )
    if not receipt_share:
        return jsonify({"msg": "Receipt share for user not found"}), 404

    try:
        receipt_share.paid = float(receipt_share.paid) - float(payment.amount)
    except Exception:
        return jsonify({"msg": "Error updating receipt share"}), 500

    for item in receipt.items:
        if item.payer_id == current_user_id and float(item.expense_cost) == float(
            payment.amount
        ):
            item.payer_id = None
            break

    db.session.delete(payment)
    db.session.commit()

    return (
        jsonify({"msg": "Payment deleted successfully", "paid": receipt_share.paid}),
        200,
    )


@receipt_bp.route("/<int:receipt_id>", methods=["DELETE"])
@jwt_required()
def delete_receipt(receipt_id):
    current_user_id = int(get_jwt_identity())

    receipt = Receipts.query.get(receipt_id)
    if not receipt:
        return jsonify({"msg": "Receipt not found"}), 404

    household = Households.query.get(receipt.household_id)
    if not household:
        return jsonify({"msg": "Household not found"}), 404

    if household.owner_id != current_user_id:
        return jsonify({"msg": "Only the household owner can delete receipts"}), 403

    db.session.delete(receipt)
    db.session.commit()
    return jsonify({"msg": "Receipt deleted successfully"}), 200
