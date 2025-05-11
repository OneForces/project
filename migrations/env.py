from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import sys
import os

# Добавляем путь до проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импорт моделей
from database.models import db

# Настройки логгера
config = context.config
fileConfig(config.config_file_name)

# Передаём метаданные в Alembic
target_metadata = db.metadata
