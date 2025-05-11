import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root'  # или '' если без пароля
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE project_db")
print("База данных 'project_db' создана.")

cursor.close()
conn.close()
