import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='my_project'
    )
    print("✅ Подключение успешно!")
    conn.close()
except Exception as e:
    print("❌ Ошибка подключения:", e)
