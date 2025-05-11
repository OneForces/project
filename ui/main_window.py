# main_window.py
import os
from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget
from ui.main_window_ui import Ui_MainWindow
from ui.stage_widget import StageWidget
from ui.received_assignments_widget import ReceivedAssignmentsWidget
from ui.notifications_widget import NotificationsWidget
from ui.history_widget import HistoryWidget
from ui.select_service_widget import SelectServiceWidget
from ui.my_sent_widget import MySentWidget

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, user):  # ⬅️ Теперь передаём объект User
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Система управления этапами")
        self.current_user = user
        self.central_stack = self.stack

        # Навигация
        self.my_sent_form = MySentWidget(self.current_user)
        self.notifications_form = NotificationsWidget(self.current_user)
        self.history_form = HistoryWidget()
        self.select_service_form = SelectServiceWidget()

        self.central_stack.addWidget(self.my_sent_form)
        self.central_stack.addWidget(self.notifications_form)
        self.central_stack.addWidget(self.history_form)
        self.central_stack.addWidget(self.select_service_form)

        nav_bar = QHBoxLayout()
        container = QWidget()
        container.setLayout(nav_bar)
        self.verticalLayout.insertWidget(0, container)

        # 🔹 Имя пользователя слева
        user_label = QPushButton(f"{self.current_user.full_name} ({self.current_user.role})")
        user_label.setEnabled(False)
        user_label.setStyleSheet("text-align: left; border: none; font-weight: bold;")
        nav_bar.addWidget(user_label)

        # 🔹 Кнопка "Выход"
        logout_btn = QPushButton("🚪 Выйти")
        logout_btn.clicked.connect(self.logout)
        nav_bar.addWidget(logout_btn)

        # Остальные кнопки
        btn_stage = QPushButton("📂 Этапы")
        btn_stage.clicked.connect(lambda: self.load_stage(1))
        nav_bar.addWidget(btn_stage)

        btn_incoming = QPushButton("📥 Входящие")
        btn_incoming.clicked.connect(self.load_stage_for_employee)
        nav_bar.addWidget(btn_incoming)

        btn_notifications = QPushButton("🔔 Уведомления")
        btn_notifications.clicked.connect(lambda: self.show_form(self.notifications_form))
        nav_bar.addWidget(btn_notifications)

        btn_history = QPushButton("📜 История")
        btn_history.clicked.connect(lambda: self.show_form(self.history_form))
        nav_bar.addWidget(btn_history)

        btn_letters = QPushButton("✉ Письмо")
        btn_letters.clicked.connect(lambda: self.show_form(self.select_service_form))
        nav_bar.addWidget(btn_letters)

        btn_sent = QPushButton("📤 Мои отправки")
        btn_sent.clicked.connect(lambda: self.show_form(self.my_sent_form))
        nav_bar.addWidget(btn_sent)


        if self.current_user.role == "Главный конструктор":
            self.load_stage(1)
        else:
            self.load_stage_for_employee()

    def show_form(self, form):
        self.central_stack.setCurrentWidget(form)

    def load_users_for_stage(self):
        from core import app
        from database.models import User
        with app.app_context():
            return User.query.filter(User.role != "Главный конструктор").all()

    def load_stage(self, stage_id):
        from types import SimpleNamespace
        stage_data = {'name': f"Этап {stage_id}", 'deadline': '2025-12-31'}
        self.current_stage = SimpleNamespace(id=stage_id)
        self.stage_form = StageWidget(stage_data, current_user=self.current_user)
        self.stage_form.populate_user_table(self.load_users_for_stage())
        self.central_stack.addWidget(self.stage_form)
        self.show_form(self.stage_form)

    def load_stage_for_employee(self):
        self.received_assignments_form = ReceivedAssignmentsWidget(self.current_user)
        self.central_stack.addWidget(self.received_assignments_form)
        self.show_form(self.received_assignments_form)

    def logout(self):
        from ui.login_window import LoginWindow
        if os.path.exists("session.json"):
            os.remove("session.json")
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()