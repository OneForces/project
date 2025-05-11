from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database.models import User
from core import app
from werkzeug.security import check_password_hash
from ui.main_window import MainWindow
from ui.register_window import RegisterWindow
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5 import QtWidgets
import json

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

        # Кнопка-глазик
        self.toggle_password_btn = QPushButton("👁")
        self.toggle_password_btn.setCheckable(True)
        self.toggle_password_btn.setFixedWidth(30)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)

        # Объединяем поле и глазик в горизонтальный layout
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

        from database.models import User
        from werkzeug.security import check_password_hash
        from core import db

        with app.app_context():  # ⬅️ вот это добавляем
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password_hash, password):
                QMessageBox.information(self, "Успех", f"Добро пожаловать, {user.full_name}")
                with open("session.json", "w") as f:
                    json.dump({"user_id": user.id}, f)

                from ui.main_window import MainWindow
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
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)