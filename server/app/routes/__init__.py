# server/app/routes
from .auth import auth_bp
from .frontend import frontend_bp


def register_routes(app):

    # FRONTEND BUILD FILES
    app.register_blueprint(frontend_bp)

    # AUTHENTICATION
    app.register_blueprint(auth_bp)
