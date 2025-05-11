import mysql.connector

# Подключение к базе
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='project_db', 
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES;")
tables = [row[0] for row in cursor.fetchall()]
print("Таблицы в базе данных:", tables)

# Добавление поля deadline в таблицу assignments
try:
    cursor.execute("ALTER TABLE assignments ADD COLUMN deadline DATE;")
    print("✅ Поле 'deadline' добавлено.")
except mysql.connector.Error as err:
    print(f"⚠️ Ошибка или поле уже существует: {err}")

conn.commit()
cursor.close()
conn.close()
