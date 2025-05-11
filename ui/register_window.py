from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from werkzeug.security import generate_password_hash
from database.models import User
from core import db
from sqlalchemy.exc import IntegrityError
from core import app, db

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание аккаунта")
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        layout.addWidget(self.username_input)

        # создаём и добавляем остальные поля
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

        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText("ФИО")
        layout.addWidget(self.full_name_input)

        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Должность")
        layout.addWidget(self.role_input)

        self.submit_btn = QPushButton("Создать аккаунт")
        self.submit_btn.clicked.connect(self.register_user)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def add_eye(self, line_edit, layout):
        eye_btn = QPushButton()
        eye_btn.setCheckable(True)
        eye_btn.setFixedWidth(30)
        eye_btn.setIcon(QIcon("eye.png"))
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
        username = self.username_input.text().strip()
        password = self.password_input.text()
        repeat = self.repeat_input.text()
        regcode = self.regcode_input.text().strip()
        full_name = self.full_name_input.text().strip()
        role = self.role_input.text().strip()

        if not all([username, password, repeat, regcode, full_name, role]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        if password != repeat:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return

        with app.app_context():
            if role == "Главный конструктор":
                existing = User.query.filter_by(role="Главный конструктор").first()
                if existing:
                    QMessageBox.warning(self, "Ошибка", "Главный конструктор уже существует")
                    return

            try:
                new_user = User(
                    username=username,
                    password_hash=generate_password_hash(password),
                    full_name=full_name,
                    role=role,
                    position=role
                )
                db.session.add(new_user)
                db.session.commit()
                QMessageBox.information(self, "Успех", "Пользователь создан!")
                self.close()
            except IntegrityError:
                db.session.rollback()
                QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует")

    def toggle_echo_mode(self, line_edit, button):
        if button.isChecked():
            line_edit.setEchoMode(QLineEdit.Normal)
        else:
            line_edit.setEchoMode(QLineEdit.Password)

