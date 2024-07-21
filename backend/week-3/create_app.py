import flask_login
from flask import Flask
from flask_login import LoginManager
from database import Staff
import dotenv
import os


def create_app():
    app = Flask(__name__)
    dotenv.load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.secret_key = os.getenv('SECRET_KEY')
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Staff.query.get(user_id)

    return app, login_manager