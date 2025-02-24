from .auth import auth_bp
from .frontend import frontend_bp
from .household_routes import household_bp
from .receipt_routes import receipt_bp
from .user_routes import user_bp


def register_routes(app):

    app.register_blueprint(frontend_bp)

    app.register_blueprint(auth_bp)

    app.register_blueprint(user_bp)

    app.register_blueprint(household_bp)

    app.register_blueprint(receipt_bp)
