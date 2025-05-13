import pymysql
import mysql.connector
from db_instance import db
from flask_app import app
from database.models import User, Stage, Assignment, AssignmentStatus
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy import inspect

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

        # 👇 Проверка наличия таблицы 'letters'
        inspector = inspect(db.engine)
        if 'letters' not in inspector.get_table_names():
            print("⚠️ Таблица 'letters' не найдена — проверь модель Letter.")
        else:
            print("✅ Таблица 'letters' присутствует.")
        
        # Этапы
        if not Stage.query.first():
            stages = [
                Stage(id=1, name='Этап 1', deadline=datetime(2025, 12, 31)),
                Stage(id=4, name='Этап 4', deadline=datetime(2025, 12, 31)),
                Stage(id=7, name='Этап 7', deadline=datetime(2025, 12, 31)),
            ]
            db.session.bulk_save_objects(stages)
            print("📌 Этапы добавлены")

        # Пользователи
        if not User.query.first():
            users = [
                User(username='gk', password_hash=generate_password_hash('gk'), full_name='Паханов Пахан', role='Главный конструктор', position='Главный конструктор'),
                User(username='dev1', password_hash=generate_password_hash('dev1'), full_name='Иванов Иван', role='Разработчик', position='Разработчик'),
                User(username='dev2', password_hash=generate_password_hash('dev2'), full_name='Петров Пётр', role='Разработчик', position='Разработчик'),
            ]
            db.session.bulk_save_objects(users)
            print("👥 Пользователи добавлены")

        # Тестовое задание
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
                status=AssignmentStatus.SENT
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

    def ensure_column(cursor, table_name: str, column_name: str, column_type: str):
        query = """
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_schema = %s AND table_name = %s AND column_name = %s;
        """
        cursor.execute(query, ('project_db', table_name, column_name))
        exists = cursor.fetchone()[0]

        if not exists:
            ddl = f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {column_type};"
            cursor.execute(ddl)
            print(f"✅ Поле '{column_name}' добавлено в таблицу '{table_name}'.")
        else:
            print(f"⚠️ Поле '{column_name}' уже существует в таблице '{table_name}'.")

    # 👇 исправленные вызовы
    ensure_column(cursor, 'assignments', 'review_comment', 'TEXT')
    ensure_column(cursor, 'assignments', 'reviewed_at', 'DATETIME')
    ensure_column(cursor, 'assignments', 'status', "ENUM('SENT','ACCEPTED','REJECTED') DEFAULT 'SENT'")

    # Обновление старых значений (если есть)
    cursor.execute("UPDATE assignments SET status='SENT' WHERE status='отправлено';")
    cursor.execute("UPDATE assignments SET status='ACCEPTED' WHERE status='принято';")
    cursor.execute("UPDATE assignments SET status='REJECTED' WHERE status='отклонено';")
    print("✅ Старые значения ENUM приведены к новым.")

    # Принудительно заменить ENUM на корректный
    cursor.execute("""
        ALTER TABLE assignments
        MODIFY COLUMN status ENUM('SENT','ACCEPTED','REJECTED') DEFAULT 'SENT';
    """)
    print("✅ Поле 'status' приведено к ENUM Python-модели.")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("🚀 Запуск инициализации проекта...")
    create_database()
    update_schema_if_needed()             # ⬅️ Сначала патчим таблицу
    initialize_sqlalchemy_models()        # ⬅️ Потом читаем/добавляем данные
    print("🎉 Готово.")