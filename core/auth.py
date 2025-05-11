from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

# Далее — маршруты:
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return "Форма входа"
