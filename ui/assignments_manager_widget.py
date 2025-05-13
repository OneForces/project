from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox, QPushButton, QLabel, QLineEdit
from sqlalchemy.orm import subqueryload
from database.models import Assignment, User, db
from ui.roles_module_combined import log_action, ROUTING_RULES 
from datetime import datetime
import os
import shutil
from flask_app import app
import subprocess
from database.models import AssignmentStatus
from core.utils.deadline import recalculate_deadline


class AssignmentsManagerWidget(QtWidgets.QWidget):
    def __init__(self, current_user, stage_data=None, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.stage_data = stage_data
        self.stage_id = stage_data.get("id", 1) if stage_data else 1
        self.attached_file_path = None

        self.layout = QtWidgets.QVBoxLayout(self)

        # Заголовок
        self.title = QLabel(f"📤 Этап {self.stage_id} - Рассылка заданий")
        self.layout.addWidget(self.title)
        if self.stage_id in [4, 7]:
            self.title.setText(f"🧩 Этап {self.stage_id} — Специальная проверка")
            special_label = QLabel("📌 Обратите внимание: для этапов 4 и 7 требуется особая форма проверки.")
            special_label.setStyleSheet("color: red; font-weight: bold;")
            self.layout.addWidget(special_label)

        # Кнопка прикрепления файла
        self.attachButton = QPushButton("📎 Прикрепить файл")
        self.attachButton.clicked.connect(self.attach_file)
        self.layout.addWidget(self.attachButton)

        self.attachedFilesLabel = QLabel("Файл не выбран")
        self.layout.addWidget(self.attachedFilesLabel)

        # Кнопка отправки
        if self.stage_id not in [4, 7]:
            self.sendButton = QPushButton("📨 Отправить задания")
            self.sendButton.clicked.connect(self.send_assignments)
            self.layout.addWidget(self.sendButton)

            # Таблица пользователей для отправки
            self.user_table = QtWidgets.QTableWidget()
            self.user_table.setColumnCount(4)
            self.user_table.setHorizontalHeaderLabels(["Выбрать", "ФИО", "Имя", "Должность"])
            self.layout.addWidget(self.user_table)
            self.load_users()

        # Таблица заданий
        self.layout.addWidget(QLabel("📥 Входящие и исходящие задания"))
        self.table = QtWidgets.QTableWidget()
        self.layout.addWidget(self.table)
        self.load_assignments()

    def load_users(self):
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

                checkbox = QTableWidgetItem()
                checkbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                checkbox.setCheckState(QtCore.Qt.Unchecked)
                checkbox.setData(QtCore.Qt.UserRole, user)

                full_info = f"{user.full_name} ({user.role})"
                self.user_table.setItem(row, 0, checkbox)
                self.user_table.setItem(row, 1, QTableWidgetItem(full_info))
                self.user_table.setItem(row, 2, QTableWidgetItem(user.username or "—"))
                self.user_table.setItem(row, 3, QTableWidgetItem(user.position or user.role or "—"))

            self.user_table.resizeColumnsToContents()

    def get_selected_users(self):
        selected = []
        for row in range(self.user_table.rowCount()):
            item = self.user_table.item(row, 0)
            if item and item.checkState() == QtCore.Qt.Checked:
                selected.append(item.data(QtCore.Qt.UserRole))
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
                    status=AssignmentStatus.SENT,
                    deadline=recalculate_deadline(self.stage_id)
                )
                db.session.add(a)
            db.session.commit()

        QMessageBox.information(self, "Готово", "Задания отправлены.")
        self.attached_file_path = None
        self.attachedFilesLabel.setText("Файл не выбран")
        self.load_assignments()

    def load_assignments(self):
        from database.models import AssignmentStatus

        with app.app_context():
            self.assignments = Assignment.query.options(
                subqueryload(Assignment.sender),
                subqueryload(Assignment.receiver),
                subqueryload(Assignment.stage)
            ).filter(
                (Assignment.receiver_id == self.current_user.id) | (Assignment.sender_id == self.current_user.id)
            ).order_by(Assignment.sent_at.desc()).all()

        self.table.setRowCount(len(self.assignments))
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "Этап", "Отправитель", "Получатель", "Файл", "Ответ", "Дедлайн",
            "Статус", "Комментарий", "Открыть", "Ответить", "Действия"
        ])

        for row, a in enumerate(self.assignments):
            self.table.setItem(row, 0, QTableWidgetItem(getattr(a.stage, "name", "—")))
            self.table.setItem(row, 1, QTableWidgetItem(getattr(a.sender, "full_name", "—")))
            self.table.setItem(row, 2, QTableWidgetItem(getattr(a.receiver, "full_name", "—")))
            self.table.setItem(row, 3, QTableWidgetItem(a.file_path or "—"))
            self.table.setItem(row, 4, QTableWidgetItem(a.response_file or "—"))

            # Дедлайн
            deadline_str = a.deadline.strftime('%Y-%m-%d') if a.deadline else "—"
            deadline_item = QTableWidgetItem(deadline_str)
            if a.deadline and a.deadline < datetime.today().date():
                deadline_item.setForeground(QtCore.Qt.red)
            self.table.setItem(row, 5, deadline_item)

            # Статус
            status_item = QTableWidgetItem(a.status.value if hasattr(a.status, "value") else a.status)
            if a.status == AssignmentStatus.ACCEPTED:
                status_item.setBackground(QtCore.Qt.green)
            elif a.status == AssignmentStatus.REJECTED:
                status_item.setBackground(QtCore.Qt.red)
            elif a.status == AssignmentStatus.SENT:
                status_item.setBackground(QtCore.Qt.yellow)
            self.table.setItem(row, 6, status_item)

            # Комментарий
            comment_input = QLineEdit()
            comment_input.setPlaceholderText("Комментарий (при отклонении)")
            self.table.setCellWidget(row, 7, comment_input)

            # Открыть файл
            open_btn = QPushButton("📂")
            open_btn.clicked.connect(lambda _, path=a.file_path: self.open_file(path))
            self.table.setCellWidget(row, 8, open_btn)

            # Ответить
            reply_btn = QPushButton("📤")
            reply_btn.clicked.connect(lambda _, r=row: self.reply_to_assignment(r))
            self.table.setCellWidget(row, 9, reply_btn)

            # Действия: принять/отклонить
            action_widget = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_widget.setLayout(action_layout)

            accept_btn = QPushButton("✅")
            reject_btn = QPushButton("❌")

            def make_handler(accepted, assignment_id=a.id, comment_widget=comment_input):
                def handler():
                    with app.app_context():
                        assignment = db.session.query(Assignment).get(assignment_id)
                        if not assignment:
                            return
                        if self.stage_id in [4, 7]:
                            log_action(f"Обработка этапа {self.stage_id}")
                        assignment.status = AssignmentStatus.ACCEPTED if accepted else AssignmentStatus.REJECTED
                        assignment.review_comment = None if accepted else comment_widget.text()
                        assignment.reviewed_at = datetime.utcnow()

                        # Цикл: 13 → 1
                        if accepted and assignment.stage_id == 13:
                            assignment.stage_id = 1

                        # Обновление дедлайна при отклонении
                        if not accepted:
                            assignment.deadline = recalculate_deadline(assignment.stage_id)

                        db.session.commit()

                        msg = (
                            f"✅ Ваше задание принято." if accepted
                            else f"❌ Ваше задание отклонено: {assignment.review_comment}"
                        )
                        send_notification(assignment.sender_id, msg)

                    self.load_assignments()
                return handler

            accept_btn.clicked.connect(make_handler(True))
            reject_btn.clicked.connect(make_handler(False))
            action_layout.addWidget(accept_btn)
            action_layout.addWidget(reject_btn)
            self.table.setCellWidget(row, 10, action_widget)

        self.table.resizeColumnsToContents()

    def reply_to_assignment(self, row):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл-ответ", "", "Все файлы (*.*)"
        )
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

        # Сохраняем ответ внутри контекста Flask
        from flask_app import app  # гарантируем реальный объект Flask
        with app.app_context():
            assignment.response_file   = os.path.relpath(dest_path, os.getcwd())
            assignment.sent_at         = datetime.utcnow()
            assignment.status          = AssignmentStatus.SENT
            assignment.review_comment  = None
            assignment.reviewed_at     = None
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
            else:
                subprocess.call(["xdg-open", path])
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл:\n{e}")

def send_notification(user_id: int, message: str):
    with app.app_context():
        from database.models import Notification
        notif = Notification(recipient_id=user_id, message=message, created_at=datetime.utcnow())
        db.session.add(notif)
        db.session.commit()

