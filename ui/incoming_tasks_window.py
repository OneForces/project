from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QPushButton, QTableWidgetItem
import os
from database.models import Assignment, User, Stage, db
from datetime import datetime
from core import app, db

class IncomingTasksWindow(QtWidgets.QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Входящие задания")
        self.resize(900, 400)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Этап", "Отправитель", "Файл", "Ответ", "Прикрепить", "Отправить", "Принять", "Отклонить"
        ])
        self.layout.addWidget(self.table)

        self.load_assignments()

    def load_assignments(self):
        self.table.setRowCount(0)

        with app.app_context():
            assignments = Assignment.query.filter_by(receiver_id=self.user_id).all()

            for row, assignment in enumerate(assignments):
                self.table.insertRow(row)

                stage = Stage.query.get(assignment.stage_id)
                sender = User.query.get(assignment.sender_id)

                self.table.setItem(row, 0, QTableWidgetItem(stage.name if stage else ""))
                self.table.setItem(row, 1, QTableWidgetItem(sender.full_name if sender else ""))

                open_btn = QPushButton("Открыть")
                open_btn.clicked.connect(lambda _, path=assignment.file_path: self.open_file(path))
                self.table.setCellWidget(row, 2, open_btn)

                response_item = QTableWidgetItem(assignment.response_file or "")
                self.table.setItem(row, 3, response_item)

                attach_btn = QPushButton("Прикрепить")
                attach_btn.clicked.connect(lambda _, r=row: self.attach_file(r))
                self.table.setCellWidget(row, 4, attach_btn)

                send_btn = QPushButton("Отправить")
                send_btn.clicked.connect(lambda _, a_id=assignment.id, r=row: self.send_response(a_id, r))
                self.table.setCellWidget(row, 5, send_btn)

                accept_btn = QPushButton("Принять")
                accept_btn.clicked.connect(lambda _, a_id=assignment.id: self.accept_assignment(a_id))
                self.table.setCellWidget(row, 6, accept_btn)

                reject_btn = QPushButton("Отклонить")
                reject_btn.clicked.connect(lambda _, a_id=assignment.id: self.reject_assignment(a_id))
                self.table.setCellWidget(row, 7, reject_btn)

    def open_file(self, path):
        if os.path.exists(path):
            os.startfile(path)
        else:
            QMessageBox.warning(self, "Ошибка", "Файл не найден")

    def attach_file(self, row):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if file_path:
            self.table.setItem(row, 3, QTableWidgetItem(file_path))

    def send_response(self, assignment_id, row):
        file_item = self.table.item(row, 3)
        if not file_item or not file_item.text():
            QMessageBox.warning(self, "Ошибка", "Не выбран файл для отправки")
            return

        file_path = file_item.text()

        with app.app_context():
            assignment = Assignment.query.get(assignment_id)
            assignment.response_file = file_path
            assignment.sent_at = datetime.utcnow()
            assignment.status = 'отправлено'
            db.session.commit()

        QMessageBox.information(self, "Успех", "Ответ отправлен")
        self.load_assignments()

    def accept_assignment(self, assignment_id):
        with app.app_context():
            assignment = Assignment.query.get(assignment_id)
            assignment.status = 'принято'
            db.session.commit()
        QMessageBox.information(self, "Готово", "Задание принято")
        self.load_assignments()

    def reject_assignment(self, assignment_id):
        with app.app_context():
            assignment = Assignment.query.get(assignment_id)
            assignment.status = 'на доработку'
            db.session.commit()
        QMessageBox.warning(self, "Отклонено", "Задание отправлено на доработку")
        self.load_assignments()
