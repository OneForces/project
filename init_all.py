import pymysql
import mysql.connector
from core import app, db
from database.models import User, Stage, Assignment
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_database():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root"
    )
    with conn.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS project_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
        print("✅ База данных 'project_db' создана.")
    conn.commit()
    conn.close()


def initialize_sqlalchemy_models():
    with app.app_context():
        db.create_all()
        print("✅ Все таблицы успешно созданы по моделям SQLAlchemy.")

        if not Stage.query.first():
            stages = [
                Stage(id=1, name='Этап 1', deadline=datetime(2025, 12, 31)),
                Stage(id=4, name='Этап 4', deadline=datetime(2025, 12, 31)),
                Stage(id=7, name='Этап 7', deadline=datetime(2025, 12, 31)),
            ]
            db.session.bulk_save_objects(stages)
            print("📌 Этапы добавлены")

        if not User.query.first():
            users = [
                User(username='gk', password_hash=generate_password_hash('gk'), full_name='Паханов Пахан', role='Главный конструктор', position='Главный конструктор'),
                User(username='dev1', password_hash=generate_password_hash('dev1'), full_name='Иванов Иван', role='Разработчик', position='Разработчик'),
                User(username='dev2', password_hash=generate_password_hash('dev2'), full_name='Петров Пётр', role='Разработчик', position='Разработчик'),
            ]
            db.session.bulk_save_objects(users)
            print("👥 Пользователи добавлены")

        db.session.commit()

        if not Assignment.query.first():
            sender = User.query.filter_by(username='gk').first()
            receiver = User.query.filter_by(username='dev1').first()
            stage = Stage.query.get(1)

            assignment = Assignment(
                sender_id=sender.id,
                receiver_id=receiver.id,
                stage_id=stage.id,
                file_path=None,
                response_file=None,
                status="отправлено"
            )
            db.session.add(assignment)
            print("📤 Тестовое задание добавлено")

        db.session.commit()
        print("✅ Начальные данные добавлены")


def update_schema_if_needed():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='project_db',
    )
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES;")
    tables = [row[0] for row in cursor.fetchall()]
    print("📊 Таблицы в базе данных:", tables)

    cursor.execute("""
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = 'project_db'
          AND table_name = 'assignments'
          AND column_name = 'deadline';
    """)
    exists = cursor.fetchone()[0]

    if not exists:
        cursor.execute("ALTER TABLE assignments ADD COLUMN deadline DATE;")
        print("✅ Поле 'deadline' добавлено.")
    else:
        print("⚠️ Поле 'deadline' уже существует.")

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    print("🚀 Запуск инициализации проекта...")
    create_database()
    initialize_sqlalchemy_models()
    update_schema_if_needed()
    print("🎉 Готово.")
