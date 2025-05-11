import sys
import json
from PyQt5.QtWidgets import QApplication

from core import app, db
from database.models import User
from ui.login_window import LoginWindow
from ui.main_window import MainWindow

def load_session():
    try:
        with open("session.json", "r") as f:
            data = json.load(f)
            user_id = data.get("user_id")
            if user_id:
                # Доступ к базе строго в контексте Flask-приложения
                with app.app_context():
                    return db.session.get(User, user_id)
    except Exception:
        return None

if __name__ == "__main__":
    # Создаём контекст Flask-приложения на всё время работы
    with app.app_context():
        db.create_all()  # если нужно, можно удалить после отладки

        qt_app = QApplication(sys.argv)

        user = load_session()
        if user:
            window = MainWindow(user)
        else:
            window = LoginWindow()

        window.show()
        sys.exit(qt_app.exec_())
