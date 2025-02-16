# server/app/routes
from flask import Blueprint, current_app

frontend_bp = Blueprint("frontend", __name__)


@frontend_bp.route("/")
def index():
    return current_app.send_static_file("index.html")
