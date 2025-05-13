from PyQt5 import QtWidgets
from database.models import Assignment, User
from flask import current_app
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel


class HistoryWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.layout().addWidget(QLabel("📜 История отправленных заданий"))

        self.history_area = QTextEdit()
        self.history_area.setReadOnly(True)
        self.layout().addWidget(self.history_area)

        self.refresh_button = QPushButton("🔄 Обновить")
        self.refresh_button.clicked.connect(self.load_sent_assignments)
        self.layout().addWidget(self.refresh_button)

        self.load_sent_assignments()

    def load_sent_assignments(self):
        with current_app.app_context():
            assignments = Assignment.query.order_by(Assignment.sent_at.desc()).limit(100).all()

        lines = []
        for a in assignments:
            sender = User.query.get(a.sender_id)
            receiver = User.query.get(a.receiver_id)
            stage = f"этап {a.stage_id}" if a.stage_id else "без этапа"
            date_str = a.sent_at.strftime('%d.%m.%Y в %H:%M') if a.sent_at else "неизвестно"

            line = f"📤 Отправлено от {sender.full_name if sender else '—'} пользователю {receiver.full_name if receiver else '—'} ({stage}) — {date_str}"
            lines.append(line)

        self.history_area.setText("\n\n".join(lines))


class NotificationsWidget(QtWidgets.QWidget):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.current_user = current_user

        layout = QtWidgets.QVBoxLayout(self)
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(QtWidgets.QLabel("🔔 Входящие уведомления"))
        layout.addWidget(self.table)

        self.load_notifications()

    def load_notifications(self):
        with current_app.app_context():
            incoming = Assignment.query.filter_by(receiver_id=self.current_user.id).all()
            self.table.setRowCount(len(incoming))
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["Отправитель", "Файл", "Статус"])

            for row, a in enumerate(incoming):
                sender = User.query.get(a.sender_id)
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(sender.full_name if sender else "—"))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(a.file_path or "—"))
                status = "Ожидает ответа" if not a.response_file else "✔ Отвечено"
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(status))

            self.table.resizeColumnsToContents()
