from flask import Flask

from .config import Config
from .extensions import db
from .routes import register_routes


def create_app():
    app = Flask(__name__, static_folder="dist", static_url_path="/")
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register routes/blueprints
    register_routes(app)

    return app
