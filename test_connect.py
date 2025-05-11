import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',  # пробуем без пароля
        database='my_project'  # укажи правильное имя базы
    )
    print("✅ Подключение успешно!")
    conn.close()
except Exception as e:
    print("❌ Ошибка подключения:", e)