# run.py

from app import app
from app.database import init_db

if __name__ == '__main__':
    # Создаём контекст приложения, чтобы корректно вызвать init_db()
    with app.app_context():
        init_db()

    # Запускаем Flask-приложение
    app.run(host='0.0.0.0', port=5000, debug=True)
