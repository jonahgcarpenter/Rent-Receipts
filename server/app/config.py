# server/app/
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
