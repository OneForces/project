# core/utils/deadline.py
from datetime import datetime, timedelta

def recalculate_deadline(stage_id: int):
    if 1 <= stage_id <= 3:
        return datetime.now().date() + timedelta(days=14)
    elif 4 <= stage_id <= 11:
        return datetime.now().date() + timedelta(days=3)
    else:
        return datetime.now().date() + timedelta(days=7)
