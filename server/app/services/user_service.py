from app.extensions import db
from app.models.users import User
from sqlalchemy.exc import SQLAlchemyError


def get_all_users():
    # Query all users from the database
    users = User.query.all()

    # Build a list of dictionaries excluding the password field
    return [
        {"id": user.id, "username": user.username, "email": user.email}
        for user in users
    ]


def get_user_by_id(user_id):
    """Retrieve a single user by id."""
    return User.query.get(user_id)


def create_new_user(username, email, password):
    """Creates a new user if they don't already exist."""
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return False, "Username or email already exists"

    new_user = User(username=username, email=email)
    new_user.set_password(password)  # Hash the password before storing

    try:
        db.session.add(new_user)
        db.session.commit()
        return True, "User created successfully"
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def update_user(user_id, data):
    """Update an existing user with the provided data."""
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    # Update the fields if they are provided
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.set_password(data["password"])

    try:
        db.session.commit()
        return True, "User updated successfully"
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)


def delete_user(user_id):
    """Delete an existing user by id."""
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    try:
        db.session.delete(user)
        db.session.commit()
        return True, "User deleted successfully"
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, str(e)
