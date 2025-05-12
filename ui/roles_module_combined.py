from PyQt5 import QtWidgets
from database.models import User, ActionLog, db
from datetime import datetime
from flask_app import app  # импортируй готовый app
from db_instance import db

# === Диалог выбора роли ===
class RoleDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор роли")
        self.setFixedSize(300, 100)

        layout = QtWidgets.QVBoxLayout(self)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItems([
            "Главный конструктор", "Инженер", "Проектировщик",
            "Разработчик", "Программист", "Конструктор", "Экономист",
            "Сотрудник КТС", "Технолог", "Метролог", "Сотрудник ПДО",
            "Сотрудник нормоконтроля", "Сотрудник КС", "Секретарь",
            "Сотрудник отдела гостайны", "Начальник центра",
            "Заместитель генерального директора", "Генеральный директор"
        ])
        layout.addWidget(QtWidgets.QLabel("Выберите роль:"))
        layout.addWidget(self.combo)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def get_role(self):
        return self.combo.currentText()


# === Правила маршрутизации ролей/должностей ===
ROUTING_RULES = {
    "Главный конструктор": [
        "Разработчик", "Программист", "Конструктор", "Сотрудник КТС", "Экономист",
        "Технолог", "Метролог", "Сотрудник ПДО", "Сотрудник нормоконтроля", "Сотрудник КС",
        "Секретарь", "Сотрудник отдела гостайны", "Начальник центра", "Заместитель генерального директора"
    ],
    "Разработчик": ["Программист", "Конструктор"],
    "Программист": ["Разработчик"],
    "Конструктор": ["Разработчик"],
    "Сотрудник КТС": ["Экономист"],
    "Экономист": ["Сотрудник КТС"],
    "Технолог": ["Метролог"],
    "Метролог": ["Технолог"],
    "Сотрудник ПДО": ["Конструктор", "Сотрудник нормоконтроля"],
    "Сотрудник нормоконтроля": ["Сотрудник ПДО"],
    "Сотрудник КС": ["Секретарь"],
    "Секретарь": ["Генеральный директор"],
    "Сотрудник отдела гостайны": ["Секретарь"],
    "Начальник центра": ["Заместитель генерального директора"],
    "Заместитель генерального директора": ["Генеральный директор"],
    "Генеральный директор": [],
    "Инженер": ["Начальник отдела"],
    "Начальник отдела": ["Главный конструктор"],
}


# === Проверка, можно ли отправлять или завершать этап ===
def can_send_assignment(role):
    return role == "Главный конструктор"

def can_complete_stage(role):
    return role == "Главный конструктор"


# === Получение списка допустимых получателей от роли отправителя ===
def get_available_receivers(sender):
    allowed_positions = ROUTING_RULES.get(sender.position, [])

    if "*" in allowed_positions:
        return User.query.filter(User.id != sender.id).all()

    return User.query.filter(User.position.in_(allowed_positions)).all()


# === Логирование действий ===
def log_action(user_id, action_type, description):
    from database.models import ActionLog
    from datetime import datetime
    from flask_app import app
    from db_instance import db

    log = ActionLog(
        user_id=user_id,
        action_type=action_type,
        description=description,
        timestamp=datetime.now()
    )

    with app.app_context():
        db.session.add(log)
        db.session.commit()
