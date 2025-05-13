import os
from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget, QVBoxLayout
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate
from ui.main_window_ui import Ui_MainWindow
from ui.select_service_widget import SelectServiceWidget
from ui.assignments_manager_widget import AssignmentsManagerWidget
from ui.widgets_combined import NotificationsWidget, HistoryWidget
from ui.notifications_widget import NotificationsWidget
from datetime import datetime, timedelta
from ui.letters_widget import LettersWidget
from flask_app import app
from db_instance import db


# === CalendarWidget встроен прямо здесь ===
class CalendarWidget(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.current_stage_date = None

    def setup_ui(self):
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)

    def highlight_stage_date(self, date):
        """Выделение даты текущего этапа"""
        self.current_stage_date = date
        self.updateCells()

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        if date == self.current_stage_date:
            painter.save()
            painter.setPen(QtCore.Qt.red)
            painter.drawRect(rect)
            painter.restore()


# === MainWindow ===
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Система управления этапами")
        self.current_user = user
        self.central_stack = self.stack

        # Основные формы
        self.notifications_form = NotificationsWidget(self.current_user)
        self.history_form = HistoryWidget()
        self.select_service_form = SelectServiceWidget()
        self.letters_form = LettersWidget(self.current_user)

        self.central_stack.addWidget(self.notifications_form)
        self.central_stack.addWidget(self.history_form)
        self.central_stack.addWidget(self.select_service_form)
        self.central_stack.addWidget(self.letters_form)
        # Панель навигации
        nav_bar = QHBoxLayout()
        container = QWidget()
        container.setLayout(nav_bar)
        self.verticalLayout.insertWidget(0, container)

        user_label = QPushButton(f"{self.current_user.full_name} ({self.current_user.role})")
        user_label.setEnabled(False)
        user_label.setStyleSheet("text-align: left; border: none; font-weight: bold;")
        nav_bar.addWidget(user_label)

        logout_btn = QPushButton("🚪 Выйти")
        logout_btn.clicked.connect(self.logout)
        nav_bar.addWidget(logout_btn)

        btn_stage = QPushButton("📂 Этапы")
        btn_stage.clicked.connect(lambda: self.load_stage(1))
        nav_bar.addWidget(btn_stage)

        btn_incoming = QPushButton("📥 Задания")
        btn_incoming.clicked.connect(lambda: self.load_stage(1))
        nav_bar.addWidget(btn_incoming)

        btn_notifications = QPushButton("🔔 Уведомления")
        btn_notifications.clicked.connect(lambda: self.show_form(self.notifications_form))
        nav_bar.addWidget(btn_notifications)

        btn_history = QPushButton("📜 История")
        btn_history.clicked.connect(lambda: self.show_form(self.history_form))
        nav_bar.addWidget(btn_history)

        btn_letters = QPushButton("✉ Письмо")
        btn_letters.clicked.connect(lambda: self.show_form(self.letters_form))  # 🔄 заменено
        nav_bar.addWidget(btn_letters)

        btn_restart = QPushButton("🔄 Новый цикл")
        btn_restart.clicked.connect(self.restart_cycle)
        nav_bar.addWidget(btn_restart)

        # Загрузить этап
        self.load_stage(1)

        # === Применение глобального стиля ===
        style_path = os.path.join(os.path.dirname(__file__), "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def restart_cycle(self):
        from database.models import Assignment

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите запустить новый цикл этапов?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if confirm != QtWidgets.QMessageBox.Yes:
            return

        with app.app_context():
            # Найдём последние задания на этапе 13
            last_assignments = Assignment.query.filter_by(stage_id=13).all()
            for a in last_assignments:
                # создаём новое задание на 1 этапе для того же получателя
                new_assignment = Assignment(
                    sender_id=a.sender_id,
                    receiver_id=a.receiver_id,
                    stage_id=1,
                    file_path=None,
                    response_file=None,
                    created_at=datetime.utcnow(),
                    sent_at=None,
                    status="отправлено"
                )
                db.session.add(new_assignment)

            db.session.commit()

        QtWidgets.QMessageBox.information(self, "Успешно", "Цикл этапов начат заново.")
        self.load_stage(1)


    def show_form(self, form):
        self.central_stack.setCurrentWidget(form)

    def load_stage(self, stage_id):
        from types import SimpleNamespace
        from PyQt5.QtCore import QDate
        if 1 <= stage_id <= 3:
            deadline = datetime.now().date() + timedelta(days=14)
        elif 4 <= stage_id <= 11:
            deadline = datetime.now().date() + timedelta(days=3)
        else:
            deadline = datetime.now().date() + timedelta(days=7)
        # Примерная дата дедлайна (в будущем можно рассчитывать автоматически)
        stage_data = {
            'id': stage_id,
            'name': f"Этап {stage_id}",
            'deadline': deadline.strftime("%Y-%m-%d")
        }
        # Удаление предыдущего календаря (если есть)
        if hasattr(self, "calendar"):
            self.verticalLayout.removeWidget(self.calendar)
            self.calendar.deleteLater()
            del self.calendar

        # === Задания ===
        stage_id = stage_data.get("id", 1) if stage_data else 1

        # Можно при необходимости кастомизировать интерфейс для конкретных этапов
        if stage_id in [4, 7]:
            # Поддержка кастомных этапов
            self.assignments_form = AssignmentsManagerWidget(self.current_user, stage_data={"id": stage_id})
            self.central_stack.addWidget(self.assignments_form)
        else:
            # Общая логика для остальных этапов
            self.assignments_form = AssignmentsManagerWidget(self.current_user, stage_data=stage_data)
            self.central_stack.addWidget(self.assignments_form)


        # === Календарь ===
        self.calendar = CalendarWidget()
        deadline_str = stage_data['deadline']
        date = QDate.fromString(deadline_str, "yyyy-MM-dd")
        self.calendar.highlight_stage_date(date)
        self.verticalLayout.addWidget(self.calendar)

        # Отображение выбранной формы
        self.show_form(self.assignments_form)

    def logout(self):
        from ui.unified_full_app import LoginWindow
        if os.path.exists("session.json"):
            os.remove("session.json")
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

