# core/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config.from_pyfile(os.path.join(BASE_DIR, "..", "config.py"))
    db.init_app(app)
    return app

app = create_app()
