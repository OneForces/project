from flask import Blueprint, request, jsonify
from core import db, app
from database.models import User, RegistrationCode
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return "Форма входа"

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    position = data.get("position")
    role = data.get("role")
    password = data.get("password")
    reg_code = data.get("reg_code")

    # 🔐 Проверка кода регистрации
    code = RegistrationCode.query.filter_by(code=reg_code).first()
    if not code:
        return jsonify({"error": "Неверный код регистрации"}), 400

    # 🛡 Проверка на уникальность Главного конструктора
    if role == "Главный конструктор":
        exists = User.query.filter_by(role="Главный конструктор").first()
        if exists:
            return jsonify({"error": "Главный конструктор уже существует"}), 400

    # ✅ Хэшируем пароль и создаём пользователя
    hashed_pw = generate_password_hash(password)
    user = User(
        first_name=first_name,
        last_name=last_name,
        position=position,
        role=role,
        password_hash=hashed_pw
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Пользователь успешно зарегистрирован"})
