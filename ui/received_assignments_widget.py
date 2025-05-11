from PyQt5 import QtWidgets
from database.models import Assignment, db
from core import app, db
from core.utils.log import log_action
from datetime import datetime
import os

class ReceivedAssignmentsWidget(QtWidgets.QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.assignments = []

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(QtWidgets.QLabel("Входящие задания"))

        self.table = QtWidgets.QTableWidget()
        self.layout.addWidget(self.table)

        self.respond_button = QtWidgets.QPushButton("Отправить ответ")
        self.layout.addWidget(self.respond_button)
        self.respond_button.clicked.connect(self.send_response)

        self.load_assignments()

    def load_assignments(self):
        from database.models import Assignment
        with app.app_context():  # ВАЖНО!
            self.assignments = Assignment.query.filter_by(receiver_id=self.user.id).all()

        self.table.setRowCount(len(self.assignments))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Отправитель", "Файл", "Ответ", "Дата"])

    # рендерим таблицу
        for row, a in enumerate(self.assignments):
            sender = getattr(a.sender, "full_name", "—")
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(sender))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(a.file_path or "—"))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(a.response_file or "—"))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(
                a.created_at.strftime('%Y-%m-%d %H:%M') if a.created_at else "—"
            ))

        self.table.resizeColumnsToContents()

    def send_response(self):
        selected = self.table.selectedItems()
        if not selected:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите задание.")
            return

        row = selected[0].row()
        if row >= len(self.assignments):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Некорректный выбор строки.")
            return

        assignment = self.assignments[row]

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл-ответ", "", "Все файлы (*.*)")
        if not file_path:
            return

        dest_dir = "uploads/responses"
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, os.path.basename(file_path))
        shutil.copy(file_path, dest_path)

        with app.app_context():
            assignment.response_file = dest_path
            assignment.sent_at = datetime.utcnow()
            db.session.commit()

        log_action(
            user_id=self.user.id,
            action_type="send_response",
            description=f"Ответ на задание: {assignment.file_path}"
        )

        QtWidgets.QMessageBox.information(self, "Готово", "Ответ отправлен.")
        self.load_assignments()