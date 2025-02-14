from .frontend import frontend_bp
from .user_routes import user_bp


def register_routes(app):

    # FRONTEND BUILD FILES
    app.register_blueprint(frontend_bp)

    # USER ROUTES
    app.register_blueprint(user_bp, url_prefix="/users")
