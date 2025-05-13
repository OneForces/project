from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox
from database.models import Notification, db
from flask_app import app
from datetime import datetime

class NotificationsWidget(QtWidgets.QWidget):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("🔔 Уведомления")
        self.layout.addWidget(self.label)

        self.table = QtWidgets.QTableWidget()
        self.layout.addWidget(self.table)

        self.refresh_button = QPushButton("🔄 Обновить")
        self.refresh_button.clicked.connect(self.load_notifications)
        self.layout.addWidget(self.refresh_button)

        self.load_notifications()

    def load_notifications(self):
        with app.app_context():
            notifs = (
                db.session.query(Notification)
                .filter_by(recipient_id=self.current_user.id)
                .order_by(Notification.created_at.desc())
                .all()
            )

        self.table.setRowCount(len(notifs))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Сообщение", "Дата", "Удалить"])

        for row, notif in enumerate(notifs):
            self.table.setItem(row, 0, QTableWidgetItem(notif.message))
            self.table.setItem(row, 1, QTableWidgetItem(notif.created_at.strftime("%d.%m.%Y %H:%M")))

            delete_btn = QPushButton("🗑 Прочитано")
            delete_btn.clicked.connect(lambda _, n_id=notif.id: self.mark_as_read(n_id))
            self.table.setCellWidget(row, 2, delete_btn)

        self.table.resizeColumnsToContents()

    def mark_as_read(self, notif_id):
        with app.app_context():
            notif = db.session.query(Notification).get(notif_id)
            if notif:
                db.session.delete(notif)
                db.session.commit()
        self.load_notifications()
