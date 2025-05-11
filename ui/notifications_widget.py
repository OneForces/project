from PyQt5 import QtWidgets
from database.models import Assignment, User
from core import app, db


class NotificationsWidget(QtWidgets.QWidget):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.current_user = current_user

        layout = QtWidgets.QVBoxLayout(self)
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(QtWidgets.QLabel("Входящие уведомления"))
        layout.addWidget(self.table)

        self.load_notifications()

    def load_notifications(self):
        with app.app_context():
            incoming = Assignment.query.filter_by(receiver_id=self.current_user.id).all()
            self.table.setRowCount(len(incoming))
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["Отправитель", "Файл", "Статус"])

            for row, a in enumerate(incoming):
                sender = User.query.get(a.sender_id)
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(sender.full_name if sender else "—"))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(a.file_path))
                status = "Ожидает ответа" if not a.response_file else "✔ Отвечено"
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(status))

            self.table.resizeColumnsToContents()
