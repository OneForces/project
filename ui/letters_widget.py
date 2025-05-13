from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QTextEdit, QPushButton, QVBoxLayout, QTableWidgetItem
from flask_app import app
from database.models import db, Letter, User
from datetime import datetime
from sqlalchemy.orm import joinedload

class LettersWidget(QtWidgets.QWidget):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("📬 Отправить письмо"))

        self.subject_input = QtWidgets.QLineEdit()
        self.subject_input.setPlaceholderText("Тема письма")
        self.layout.addWidget(self.subject_input)

        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Текст письма")
        self.layout.addWidget(self.body_input)

        self.send_btn = QPushButton("📨 Отправить")
        self.send_btn.clicked.connect(self.send_letter)
        self.layout.addWidget(self.send_btn)

        self.letters_table = QtWidgets.QTableWidget()
        self.layout.addWidget(QLabel("📥 Входящие и исходящие письма"))
        self.layout.addWidget(self.letters_table)

        self.load_letters()

    def send_letter(self):
        subject = self.subject_input.text()
        body = self.body_input.toPlainText()
        receiver_id = 2  # 🔁 временно, заменить на выбор из UI

        if not subject or not body:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите тему и текст письма.")
            return

        with app.app_context():
            letter = Letter(
                sender_id=self.current_user.id,
                receiver_id=receiver_id,
                subject=subject,
                body=body
            )
            db.session.add(letter)
            db.session.commit()

        QtWidgets.QMessageBox.information(self, "Успешно", "Письмо отправлено.")
        self.subject_input.clear()
        self.body_input.clear()
        self.load_letters()

    def load_letters(self):
        with app.app_context():
            letters = Letter.query.options(
                joinedload(Letter.sender),
                joinedload(Letter.receiver)
            ).filter(
                (Letter.sender_id == self.current_user.id) |
                (Letter.receiver_id == self.current_user.id)
            ).order_by(Letter.created_at.desc()).all()

        self.letters_table.setRowCount(len(letters))
        self.letters_table.setColumnCount(4)
        self.letters_table.setHorizontalHeaderLabels(["Отправитель", "Получатель", "Тема", "Дата"])

        for row, l in enumerate(letters):
            self.letters_table.setItem(row, 0, QTableWidgetItem(l.sender.full_name))
            self.letters_table.setItem(row, 1, QTableWidgetItem(l.receiver.full_name))
            self.letters_table.setItem(row, 2, QTableWidgetItem(l.subject))
            self.letters_table.setItem(row, 3, QTableWidgetItem(str(l.created_at)))

        self.letters_table.resizeColumnsToContents()
