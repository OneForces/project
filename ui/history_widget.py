from PyQt5 import QtWidgets
from database.models import ActionLog, User
from core import app, db

class HistoryWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Пользователь", "Действие", "Описание", "Дата и время"])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.layout().addWidget(QtWidgets.QLabel("История действий"))
        self.layout().addWidget(self.table)

        self.load_logs()

    def load_logs(self):
        with app.app_context():
            logs = ActionLog.query.order_by(ActionLog.timestamp.desc()).limit(50).all()
            self.table.setRowCount(len(logs))

            for row, log in enumerate(logs):
                user = User.query.get(log.user_id)
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(user.full_name if user else "—"))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(log.action_type))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(log.description))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(
                    log.timestamp.strftime('%Y-%m-%d %H:%M') if log.timestamp else "—"))

            self.table.resizeColumnsToContents()
