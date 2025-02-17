from .auth import auth_bp
from .frontend import frontend_bp
from .household_routes import household_bp
from .user_routes import user_bp


def register_routes(app):

    # FRONTEND BUILD FILES
    app.register_blueprint(frontend_bp)

    # AUTHENTICATION
    app.register_blueprint(auth_bp)

    # USER ROUTES
    app.register_blueprint(user_bp)

    # HOUSEHOLD ROUTES
    app.register_blueprint(household_bp)
