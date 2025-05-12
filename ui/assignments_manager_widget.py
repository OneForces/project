from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox, QPushButton, QLabel
from sqlalchemy.orm import subqueryload
from database.models import Assignment, User, db
from ui.roles_module_combined import log_action
from flask import current_app as app
from ui.roles_module_combined import ROUTING_RULES
from datetime import datetime
import os
import shutil
import subprocess
from flask_app import app
from db_instance import db
from database.models import User

class AssignmentsManagerWidget(QtWidgets.QWidget):
    def __init__(self, current_user, stage_data=None, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.stage_data = stage_data
        self.stage_id = stage_data.get("id", 1) if stage_data else 1
        self.attached_file_path = None

        self.layout = QtWidgets.QVBoxLayout(self)

        # --- Верх: панель отправки ---
        self.title = QLabel(f"📤 Этап {self.stage_id} - Рассылка заданий")
        self.layout.addWidget(self.title)

        self.attachButton = QPushButton("📎 Прикрепить файл")
        self.attachButton.clicked.connect(self.attach_file)
        self.layout.addWidget(self.attachButton)

        self.attachedFilesLabel = QLabel("Файл не выбран")
        self.layout.addWidget(self.attachedFilesLabel)

        self.sendButton = QPushButton("📨 Отправить задания")
        self.sendButton.clicked.connect(self.send_assignments)
        self.layout.addWidget(self.sendButton)

        self.user_table = QtWidgets.QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["Выбрать", "ФИО", "Имя", "Должность"])
        self.layout.addWidget(self.user_table)

        self.load_users()

        # --- Низ: таблица заданий ---
        self.table = QtWidgets.QTableWidget()
        self.layout.addWidget(QtWidgets.QLabel("📥 Входящие и исходящие задания"))
        self.layout.addWidget(self.table)

        self.load_assignments()

    def load_users(self):
        from flask_app import app  # если не импортировал глобально

        self.user_table.setRowCount(0)
        allowed_roles = ROUTING_RULES.get(self.current_user.role, [])

        with app.app_context():
            users = db.session.query(User).all()

            for user in users:
                if user.id == self.current_user.id:
                    continue
                if "*" not in allowed_roles and user.role not in allowed_roles:
                    continue

                row = self.user_table.rowCount()
                self.user_table.insertRow(row)

                checkbox = QtWidgets.QTableWidgetItem()
                checkbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                checkbox.setCheckState(QtCore.Qt.Unchecked)
                checkbox.setData(QtCore.Qt.UserRole, user)

                self.user_table.setItem(row, 0, checkbox)
                self.user_table.setItem(row, 1, QtWidgets.QTableWidgetItem(user.full_name))
                self.user_table.setItem(row, 2, QtWidgets.QTableWidgetItem(""))
                self.user_table.setItem(row, 3, QtWidgets.QTableWidgetItem(user.position))

            self.user_table.resizeColumnsToContents()


    def get_selected_users(self):
        selected = []
        for row in range(self.user_table.rowCount()):
            item = self.user_table.item(row, 0)
            if item and item.checkState() == QtCore.Qt.Checked:
                user = item.data(QtCore.Qt.UserRole)
                if user:
                    selected.append(user)
        return selected

    def attach_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if file_path:
            self.attached_file_path = file_path
            self.attachedFilesLabel.setText(f"📎 Прикреплено: {os.path.basename(file_path)}")

    def send_assignments(self):
        users = self.get_selected_users()
        file_path = self.attached_file_path

        if not users or not file_path:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователей и файл.")
            return

        with app.app_context():
            for user in users:
                a = Assignment(
                    sender_id=self.current_user.id,
                    receiver_id=user.id,
                    stage_id=self.stage_id,
                    file_path=file_path,
                    response_file=None,
                    created_at=datetime.utcnow(),
                    sent_at=datetime.utcnow(),
                    status="отправлено"
                )
                db.session.add(a)
            db.session.commit()

        QMessageBox.information(self, "Готово", "Задания отправлены.")
        self.attached_file_path = None
        self.attachedFilesLabel.setText("Файл не выбран")
        self.load_assignments()

    def load_assignments(self):
        with app.app_context():
            self.assignments = Assignment.query.options(
                subqueryload(Assignment.sender),
                subqueryload(Assignment.receiver),
                subqueryload(Assignment.stage)
            ).filter(
                (Assignment.receiver_id == self.current_user.id) | (Assignment.sender_id == self.current_user.id)
            ).order_by(Assignment.sent_at.desc()).all()

        self.table.setRowCount(len(self.assignments))
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Этап", "Отправитель", "Получатель", "Файл", "Ответ", "Статус", "Открыть", "Ответить"
        ])

        for row, a in enumerate(self.assignments):
            self.table.setItem(row, 0, QTableWidgetItem(getattr(a.stage, "name", "—")))
            self.table.setItem(row, 1, QTableWidgetItem(getattr(a.sender, "full_name", "—")))
            self.table.setItem(row, 2, QTableWidgetItem(getattr(a.receiver, "full_name", "—")))
            self.table.setItem(row, 3, QTableWidgetItem(a.file_path or "—"))
            self.table.setItem(row, 4, QTableWidgetItem(a.response_file or "—"))
            self.table.setItem(row, 5, QTableWidgetItem(a.status or "Ожидание"))

            open_btn = QPushButton("📂")
            open_btn.clicked.connect(lambda _, path=a.file_path: self.open_file(path))
            self.table.setCellWidget(row, 6, open_btn)

            reply_btn = QPushButton("📤")
            reply_btn.clicked.connect(lambda _, r=row: self.reply_to_assignment(r))
            self.table.setCellWidget(row, 7, reply_btn)

        self.table.resizeColumnsToContents()

    def reply_to_assignment(self, row):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл-ответ", "", "Все файлы (*.*)")
        if not file_path:
            return

        assignment = self.assignments[row]
        dest_dir = os.path.join(os.getcwd(), "uploads", "responses")
        os.makedirs(dest_dir, exist_ok=True)

        filename = f"resp_uid{self.current_user.id}_aid{assignment.id}_{os.path.basename(file_path)}"
        dest_path = os.path.join(dest_dir, filename)

        try:
            shutil.copy(file_path, dest_path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {e}")
            return

        with app.app_context():
            assignment.response_file = os.path.relpath(dest_path, os.getcwd())
            assignment.sent_at = datetime.utcnow()
            assignment.status = "отправлено"
            db.session.commit()

        log_action(
            user_id=self.current_user.id,
            action_type="Ответ на задание",
            description="Пользователь отправил ответ на задание"
        )

        QMessageBox.information(self, "Готово", "Ответ отправлен.")
        self.load_assignments()

    def open_file(self, path):
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Ошибка", f"Файл не найден:\n{path}")
            return
        try:
            if os.name == "nt":
                os.startfile(path)
            elif os.name == "posix":
                subprocess.call(["xdg-open", path])
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл:\n{str(e)}")
