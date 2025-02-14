from app.models.users import User


def get_all_users():
    # Placeholder function; in a real application, you'd query your database:
    # Example: return [user.to_dict() for user in User.query.all()]
    return [
        {"id": 1, "username": "john_doe", "email": "john@example.com"},
        {"id": 2, "username": "jane_doe", "email": "jane@example.com"},
    ]
