from PyQt5 import QtWidgets
from database.models import Assignment, User
from core import app

class HistoryWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Отправитель", "Получатель", "Этап", "Дата отправки"])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.layout().addWidget(QtWidgets.QLabel("История отправленных заданий"))
        self.layout().addWidget(self.table)

        self.load_sent_assignments()

    def load_sent_assignments(self):
        with app.app_context():
            assignments = Assignment.query.order_by(Assignment.sent_at.desc()).limit(50).all()
            self.table.setRowCount(len(assignments))

            for row, a in enumerate(assignments):
                sender = User.query.get(a.sender_id)
                receiver = User.query.get(a.receiver_id)

                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(sender.full_name if sender else "—"))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(receiver.full_name if receiver else "—"))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(a.stage_id)))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(
                    a.sent_at.strftime('%Y-%m-%d %H:%M') if a.sent_at else "—"
                ))

            self.table.resizeColumnsToContents()
