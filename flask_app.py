import os
from flask import Flask
from db_instance import db

def create_app():
    app = Flask(__name__)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(BASE_DIR, "config.py")
    app.config.from_pyfile(config_path)
    db.init_app(app)
    return app

app = create_app()
