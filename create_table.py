import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='project_db'
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    title VARCHAR(255),
    description TEXT,
    filename VARCHAR(255),
    filepath VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deadline DATE
);
""")

print("Таблица 'assignments' создана.")

conn.commit()
cursor.close()
conn.close()
