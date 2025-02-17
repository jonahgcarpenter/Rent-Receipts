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


class HouseholdInvitation(db.Model):
    __tablename__ = "household_invitations"

    id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(
        db.Integer, db.ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    invitee_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    invited_by = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    household = db.relationship("Households", backref="invitations", lazy=True)
    invitee = db.relationship(
        "Users", foreign_keys=[invitee_id], backref="invitations_received", lazy=True
    )
    inviter = db.relationship(
        "Users", foreign_keys=[invited_by], backref="invitations_sent", lazy=True
    )

    def __repr__(self):
        return f"<HouseholdInvitation household_id={self.household_id} invitee_id={self.invitee_id}>"
