from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QTableWidgetItem, QMessageBox
from database.models import Assignment, User
from core import app
import os
import subprocess

class MySentWidget(QtWidgets.QWidget):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.current_user = current_user

        self.setLayout(QtWidgets.QVBoxLayout())
        self.title = QtWidgets.QLabel("📤 Мои отправленные задания")
        self.layout().addWidget(self.title)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Получатель", "Этап", "Файл", "Статус"])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.layout().addWidget(self.table)

        self.load_my_assignments()

    def load_my_assignments(self):
        with app.app_context():
            assignments = Assignment.query.filter_by(sender_id=self.current_user.id).order_by(Assignment.sent_at.desc()).all()
            self.table.setRowCount(len(assignments))

            for row, a in enumerate(assignments):
                receiver = User.query.get(a.receiver_id)
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(receiver.full_name if receiver else "—"))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(a.stage_id)))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(a.file_path or "—"))

                if a.response_file:
                    status = "✔ Принято"
                elif a.status == "на доработку":
                    status = "↺ На доработку"
                else:
                    status = "⏳ Ожидание"

                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(status))

            self.table.resizeColumnsToContents()

    def open_file(self, path):
        if not os.path.exists(path):
            QMessageBox.warning(self, "Ошибка", f"Файл не найден:\n{path}")
            return
        try:
            if os.name == "nt":  
                os.startfile(path)
            elif os.name == "posix":
                subprocess.call(["xdg-open", path])
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл:\n{str(e)}")
