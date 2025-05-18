import sqlite3
import os

DB_PATH = "data/numbers.db"

def create_and_fill_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER NOT NULL,
            type TEXT CHECK (type IN ('1D','2D')) NOT NULL
        )
    ''')

    # Заполняем 1D данные (арифметическая прогрессия)
    cur.execute("DELETE FROM numbers WHERE type = '1D'")
    a, d, n = 5, 3, 1000
    for i in range(n):
        val = a + i * d
        cur.execute("INSERT INTO numbers (value, type) VALUES (?, ?)", (val, '1D'))

    conn.commit()
    conn.close()