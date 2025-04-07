# app/database.py

import sqlite3
from flask import current_app
from datetime import datetime, timedelta

def get_db():
    """
    Подключение к базе данных с учётом таймаута, 
    включаем foreign_keys=ON и возвращаем объект conn.
    """
    conn = sqlite3.connect(current_app.config['DATABASE'], 
                           timeout=current_app.config['SQLITE_TIMEOUT'])
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Создаёт таблицы в базе, если они не существуют.
    """
    with current_app.app_context():
        conn = get_db()
        c = conn.cursor()

        # Если нужно: c.execute("DROP TABLE IF EXISTS records") и т.д.

        c.execute('''
            CREATE TABLE IF NOT EXISTS machines (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS drivers (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS counterparties (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY,
                date DATE NOT NULL,
                machine_id INTEGER,
                driver_id INTEGER,
                start_time TEXT,
                end_time TEXT,
                hours INTEGER DEFAULT 0,
                comment TEXT,
                counterparty_id INTEGER,
                status TEXT NOT NULL CHECK(status IN ('work', 'stop', 'repair', 'holiday')),
                FOREIGN KEY(machine_id) REFERENCES machines(id) ON DELETE SET NULL,
                FOREIGN KEY(driver_id) REFERENCES drivers(id) ON DELETE SET NULL,
                FOREIGN KEY(counterparty_id) REFERENCES counterparties(id) ON DELETE SET NULL
            )
        ''')
        conn.commit()
        conn.close()

def get_next_free_id(conn, table_name: str) -> int:
    """
    Определяет следующее свободное числовое поле id для таблицы (id начинаются с 1).
    """
    rows = conn.execute(f"SELECT id FROM {table_name} ORDER BY id").fetchall()
    used = {r[0] for r in rows}
    candidate = 1
    while candidate in used:
        candidate += 1
    return candidate
