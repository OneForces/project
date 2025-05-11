from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFileDialog, QLabel
from ui.stage_form import Ui_StageForm
import locale
import os
from core.roles_data import ROUTING_RULES


# Установка локали для русских дат
try:
    locale.setlocale(locale.LC_TIME, 'Russian_Russia')  # Windows
except:
    try:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')  # Linux/macOS
    except:
        pass

class StageWidget(QtWidgets.QWidget, Ui_StageForm):
    def __init__(self, stage_data=None, current_user=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.configure_user_table()

        self.current_user = current_user
        self.attached_file_path = None

        self.attachButton.clicked.connect(self.attach_files)
        self.sendButton.clicked.connect(self.send_assignments)

        if stage_data:
            self.setup_stage(stage_data)

    def configure_user_table(self):
        """Настройка таблицы пользователей с чекбоксами"""
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Выбрать", "Фамилия", "Имя", "Должность"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def setup_stage(self, stage_data):
        """Установка названия и срока этапа"""
        self.stageTitleLabel.setText(stage_data.get('name', 'Без названия'))

        deadline_str = stage_data.get('deadline')
        if deadline_str:
            try:
                deadline_qdate = QDate.fromString(deadline_str, 'yyyy-MM-dd')
                formatted = deadline_qdate.toString('dd MMMM yyyy')
                self.deadlineLabel.setText(f"До: {formatted}")
            except:
                self.deadlineLabel.setText("Срок (ошибка формата)")
        else:
            self.deadlineLabel.setText("Срок не установлен")

    def populate_user_table(self, users):
        self.tableWidget.setRowCount(0)

        # Получаем роль текущего пользователя
        sender_role = self.current_user.role if self.current_user else "Гость"
        allowed_roles = ROUTING_RULES.get(sender_role, [])

        for user in users:
            if self.current_user and user.id == self.current_user.id:
                continue  # нельзя отправлять себе

            if "*" not in allowed_roles and user.role not in allowed_roles:
                continue

            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)

            checkbox = QtWidgets.QTableWidgetItem()
            checkbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            checkbox.setCheckState(QtCore.Qt.Unchecked)
            checkbox.setData(QtCore.Qt.UserRole, user)

            self.tableWidget.setItem(row, 0, checkbox)
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(user.last_name))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(user.first_name))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(user.position))

        self.tableWidget.resizeColumnsToContents()


    def get_selected_users(self):
        """Получить всех отмеченных пользователей"""
        selected_users = []

        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            if item and item.checkState() == QtCore.Qt.Checked:
                user = item.data(QtCore.Qt.UserRole)
                if user:
                    selected_users.append(user)

        return selected_users

    def attach_files(self):
        """Открытие диалога и вывод выбранного файла"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if file_path:
            filename = os.path.basename(file_path)
            self.attachedFilesLabel.setText(f"Выбран: {filename}")
            self.attached_file_path = file_path  # сохранить путь
    
    def send_assignments(self):
        users = self.get_selected_users()
        file_path = self.attached_file_path

        if not users or not file_path:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите пользователей и прикрепите файл.")
            return

        sender_id = self.current_user.id if self.current_user else None
        stage_id = getattr(self.parent(), "current_stage", None)
        stage_id = stage_id.id if stage_id else 1

        with app.app_context():
            for user in users:
                assignment = Assignment(
                    sender_id=sender_id,
                    receiver_id=user.id,
                    stage_id=stage_id,
                    file_path=file_path,
                    response_file=None,
                    created_at=datetime.now(),
                    sent_at=datetime.now(),
                    status="отправлено"
                )
                db.session.add(assignment)

            db.session.commit()

        QtWidgets.QMessageBox.information(self, "Готово", "Задания отправлены.")
        self.attachedFilesLabel.setText("Файлы не выбраны")
        self.attached_file_path = None