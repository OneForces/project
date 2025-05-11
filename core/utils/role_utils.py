from database.models import User, ActionLog, db
 
from core.roles_data import ROUTING_RULES

def get_available_receivers(sender):
    """Возвращает пользователей, которым разрешено отправлять задания от текущей роли/должности."""
    allowed_positions = ROUTING_RULES.get(sender.position, [])

    if "*" in allowed_positions:
        return User.query.filter(User.id != sender.id).all()

    return User.query.filter(User.position.in_(allowed_positions)).all()


def log_action(user_id, action_type, description):
    """Сохраняет лог действия пользователя."""
    log = ActionLog(
        user_id=user_id,
        action_type=action_type,
        description=description
    )
    db.session.add(log)
    db.session.commit()

ROUTING_RULES = {
    "Инженер": ["Начальник отдела"],
    "Начальник отдела": ["Главный конструктор"],
    "Главный конструктор": ["*"]
}

def get_available_receivers(sender):
    allowed_positions = ROUTING_RULES.get(sender.position, [])

    if "*" in allowed_positions:
        return User.query.filter(User.id != sender.id).all()

    return User.query.filter(User.position.in_(allowed_positions)).all()