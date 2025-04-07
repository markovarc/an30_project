# app/__init__.py

from flask import Flask

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # ваш секретный ключ
app.config['DATABASE'] = 'an30.db'    # имя файла с базой данных
app.config['SQLITE_TIMEOUT'] = 20

# Импортируем здесь же наши роуты,
# чтобы они зарегистрировались на объекте app
from . import routes
