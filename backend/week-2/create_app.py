from flask import Flask
import dotenv
import os


def create_app():
    app = Flask(__name__)
    dotenv.load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    return app