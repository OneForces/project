& "C:\tools\mysql\current\bin\mysqld.exe" --console --verbose --log-error="C:\mysql_start_error.log" - Запуск MySQL (Первое окно powershell от имени администратора).
mysql -u root -p Вход в MySQL (Второе окно powershell от имени администратора).
root - базовый пароль.

Запуск проекта.
git clone https://github.com/OneForces/project
python -m venv venv
source ./venv/Scripts/activate
pip install -r requirements.txt
python init_all.py (Сработает только после успешного подключения к БД.)
python app_final_combined.py (Запуск проекта.)

