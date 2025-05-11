from database.models import ActionLog, db
from datetime import datetime

def log_action(user_id, action_type, description):
    log = ActionLog(
        user_id=user_id,
        action_type=action_type,
        description=description,
        timestamp=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()
