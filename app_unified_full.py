import sys
import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from PyQt5.QtWidgets import QApplication
from database.models import User
from ui.main_window import MainWindow
from ui.unified_full_app import LoginWindow


# === 🔧 Поиск qwindows.dll (встроено из find_qwindows.py) ===
def find_qwindows_dll():
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        if "qwindows.dll" in files:
            break


# === ⚙️ Flask-приложение и SQLAlchemy ===
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")  # путь к твоему конфигу
    db.init_app(app)
    return app

app = create_app()


# === 🔐 Загрузка текущей сессии
def load_session():
    try:
        with open("session.json", "r") as f:
            user_id = json.load(f).get("user_id")
            if user_id:
                with app.app_context():
                    return db.session.get(User, user_id)
    except:
        pass
    return None


# === 🚀 Запуск приложения
if __name__ == "__main__":
    find_qwindows_dll()  # отладка Qt
    qt_app = QApplication(sys.argv)
    with app.app_context():
        user = load_session()
        window = MainWindow(user) if user else LoginWindow()
        window.show()
    sys.exit(qt_app.exec_())
