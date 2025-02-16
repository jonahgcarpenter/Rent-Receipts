# server/app/
from flask import Flask

from .config import Config
from .extensions import db, jwt
from .routes import register_routes


def create_app():
    app = Flask(__name__, static_folder="dist", static_url_path="/")
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    register_routes(app)

    return app
