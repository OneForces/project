# init_db.py
from core import app, db
from database.models import User, Stage
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    with app.app_context():
        db.create_all()
        print("✅ Все таблицы успешно созданы по моделям SQLAlchemy.")

        # Этапы (если нет, добавляем)
        if not Stage.query.first():
            stages = [
                Stage(id=1, name='Этап 1', deadline=datetime(2025, 12, 31)),
                Stage(id=4, name='Этап 4', deadline=datetime(2025, 12, 31)),
                Stage(id=7, name='Этап 7', deadline=datetime(2025, 12, 31)),
            ]
            db.session.bulk_save_objects(stages)
            print("📌 Этапы добавлены")

        # Тестовые пользователи (если нет, добавляем)
        if not User.query.first():
            users = [
                User(username='gk', password_hash=generate_password_hash('gk'), full_name='Паханов Пахан', role='Главный конструктор', position='Главный конструктор'),
                User(username='dev1', password_hash=generate_password_hash('dev1'), full_name='Иванов Иван', role='Разработчик', position='Разработчик'),
                User(username='dev2', password_hash=generate_password_hash('dev2'), full_name='Петров Пётр', role='Разработчик', position='Разработчик'),
            ]
            db.session.bulk_save_objects(users)
            print("👥 Пользователи добавлены")

        db.session.commit()
        print("✅ Начальные данные добавлены")

if __name__ == "__main__":
    init_database()
