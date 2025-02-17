from app import db
from app.models.users import Users


class Households(db.Model):
    __tablename__ = "households"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    owner_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    users = db.relationship(
        "Users", foreign_keys=[Users.household_id], backref="household", lazy=True
    )
    owner = db.relationship("Users", foreign_keys=[owner_id], backref="owned_household")
