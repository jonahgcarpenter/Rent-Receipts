from app import db


class Receipts(db.Model):
    __tablename__ = "receipts"
    id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(
        db.Integer, db.ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    items = db.relationship(
        "ReceiptItems", backref="receipt", lazy=True, cascade="all, delete-orphan"
    )
    shares = db.relationship(
        "ReceiptShares", backref="receipt", lazy=True, cascade="all, delete-orphan"
    )
    payments = db.relationship(
        "Payments", backref="receipt", lazy=True, cascade="all, delete-orphan"
    )


class ReceiptItems(db.Model):
    __tablename__ = "receipt_items"
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(
        db.Integer, db.ForeignKey("receipts.id", ondelete="CASCADE"), nullable=False
    )
    expense_name = db.Column(db.String(256), nullable=False)
    expense_cost = db.Column(db.Numeric(10, 2), nullable=False)
    payer_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    payer = db.relationship("Users", backref=db.backref("receipt_items", lazy=True))


class ReceiptShares(db.Model):
    __tablename__ = "receipt_shares"
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(
        db.Integer, db.ForeignKey("receipts.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    share = db.Column(db.Numeric(10, 2), nullable=False)
    paid = db.Column(db.Numeric(10, 2), default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    __table_args__ = (
        db.UniqueConstraint("receipt_id", "user_id", name="uq_receipt_user"),
    )

    user = db.relationship("Users", backref=db.backref("receipt_shares", lazy=True))


class Payments(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(
        db.Integer, db.ForeignKey("receipts.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship("Users", backref=db.backref("payments", lazy=True))
