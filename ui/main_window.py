from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget
from types import SimpleNamespace
from ui.main_window_ui import Ui_MainWindow
from ui.stage_widget import StageWidget
from ui.received_assignments_widget import ReceivedAssignmentsWidget
from ui.notifications_widget import NotificationsWidget
from ui.history_widget import HistoryWidget
from ui.select_service_widget import SelectServiceWidget
from database.models import User
from core import app

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, user_role):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Система управления этапами")
        self.current_user = SimpleNamespace(id=1, full_name="Главный Пользователь", role=user_role)

        # Внутренний стек виджетов
        self.central_stack = self.stack  # привязка к QStackedWidget из .ui

        # Подключаем формы
        self.notifications_form = NotificationsWidget(self.current_user)
        self.history_form = HistoryWidget()
        self.select_service_form = SelectServiceWidget()

        self.central_stack.addWidget(self.notifications_form)
        self.central_stack.addWidget(self.history_form)
        self.central_stack.addWidget(self.select_service_form)

        # Навигация
        nav_bar = QHBoxLayout()
        container = QWidget()
        container.setLayout(nav_bar)
        self.verticalLayout.insertWidget(0, container)

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

        # Загрузка начального интерфейса
        if self.current_user.role == "Главный конструктор":
            self.load_stage(1)
        else:
            self.load_stage_for_employee()

    def show_form(self, form):
        self.central_stack.setCurrentWidget(form)

    def load_users_for_stage(self):
        with app.app_context():
            return User.query.filter(User.role != "Главный конструктор").all()

    def load_stage(self, stage_id):
        stage_data = {'name': f"Этап {stage_id}", 'deadline': '2025-12-31'}
        self.current_stage = SimpleNamespace(id=stage_id)

        self.stage_form = StageWidget(stage_data)
        self.stage_form.populate_user_table(self.load_users_for_stage())

        self.central_stack.addWidget(self.stage_form)
        self.show_form(self.stage_form)

    def load_stage_for_employee(self):
        self.received_assignments_form = ReceivedAssignmentsWidget(self.current_user)
        self.central_stack.addWidget(self.received_assignments_form)
        self.show_form(self.received_assignments_form)
