import sys
import os
import json
import threading
import requests
from flask import Flask, Blueprint, request, jsonify
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QHBoxLayout, QLineEdit
)
from PyQt5.QtGui import QIcon
from werkzeug.security import generate_password_hash, check_password_hash
from core import app, db
from sqlalchemy.exc import IntegrityError
from database.models import User, RegistrationCode
from ui.main_window import MainWindow

# === Flask API ===
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    position = data.get("position")
    role = data.get("role")
    password = data.get("password")
    reg_code = data.get("reg_code")

    code = RegistrationCode.query.filter_by(code=reg_code).first()
    if not code:
        return jsonify({"error": "Неверный код регистрации"}), 400

    if role == "Главный конструктор":
        exists = User.query.filter_by(role="Главный конструктор").first()
        if exists:
            return jsonify({"error": "Главный конструктор уже существует"}), 400

    hashed_pw = generate_password_hash(password)
    user = User(
        full_name=f"{first_name} {last_name}",
        position=position,
        role=role,
        password_hash=hashed_pw,
        username=f"{first_name.lower()}.{last_name.lower()}"
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Пользователь успешно зарегистрирован"})

@auth_bp.route('/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return jsonify({"message": "ok", "user_id": user.id})
    return jsonify({"error": "Неверный логин или пароль"}), 401

def run_flask():
    flask_app = Flask(__name__)
    flask_app.register_blueprint(auth_bp)
    flask_app.app_context().push()
    flask_app.run(port=5000, debug=False, use_reloader=False)

# === RegisterWindow ===
class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание аккаунта")
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Имя")
        layout.addWidget(self.first_name_input)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Фамилия")
        layout.addWidget(self.last_name_input)

        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText("Должность")
        layout.addWidget(self.position_input)

        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Роль")
        layout.addWidget(self.role_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.add_eye(self.password_input, layout)

        self.repeat_input = QLineEdit()
        self.repeat_input.setPlaceholderText("Повторите пароль")
        self.repeat_input.setEchoMode(QLineEdit.Password)
        self.add_eye(self.repeat_input, layout)

        self.regcode_input = QLineEdit()
        self.regcode_input.setPlaceholderText("Код регистрации")
        self.regcode_input.setEchoMode(QLineEdit.Password)
        self.add_eye(self.regcode_input, layout)

        self.submit_btn = QPushButton("Создать аккаунт")
        self.submit_btn.clicked.connect(self.register_user)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def add_eye(self, line_edit, layout):
        eye_btn = QPushButton("👁")
        eye_btn.setCheckable(True)
        eye_btn.setFixedWidth(30)
        eye_btn.setStyleSheet("border: none;")
        eye_btn.clicked.connect(lambda checked: line_edit.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password))

        container = QHBoxLayout()
        container.addWidget(line_edit)
        container.addWidget(eye_btn)

        wrapper = QWidget()
        wrapper.setLayout(container)
        layout.addWidget(wrapper)

    def register_user(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        position = self.position_input.text().strip()
        role = self.role_input.text().strip()
        password = self.password_input.text()
        repeat = self.repeat_input.text()
        reg_code = self.regcode_input.text().strip()

        if not all([first_name, last_name, position, role, password, repeat, reg_code]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        if password != repeat:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "position": position,
            "role": role,
            "password": password,
            "reg_code": reg_code
        }

        try:
            response = requests.post("http://localhost:5000/register", json=payload)
            if response.status_code == 200:
                QMessageBox.information(self, "Готово", "Пользователь создан!")
                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", response.json().get("error", "Ошибка регистрации"))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка подключения: {e}")

# === LoginWindow ===
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.toggle_password_btn = QPushButton("👁")
        self.toggle_password_btn.setCheckable(True)
        self.toggle_password_btn.setFixedWidth(30)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_btn)

        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.login)

        self.register_btn = QPushButton("Регистрация")
        self.register_btn.clicked.connect(self.open_register)

        layout.addWidget(QLabel("Добро пожаловать"))
        layout.addWidget(self.username_input)
        layout.addLayout(password_layout)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        with app.app_context():
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password_hash, password):
                QMessageBox.information(self, "Успех", f"Добро пожаловать, {user.full_name}")
                with open("session.json", "w") as f:
                    json.dump({"user_id": user.id}, f)

                self.main_window = MainWindow(user)
                self.main_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def open_register(self):
        self.reg_window = RegisterWindow()
        self.reg_window.show()

    def toggle_password_visibility(self):
        if self.toggle_password_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

# === Запуск ===
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    qt_app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(qt_app.exec_())
