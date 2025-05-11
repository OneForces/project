# init_db_full.py
from core import app, db
from database import models  

with app.app_context():
    db.create_all()
    print("✅ Все таблицы созданы.")
