import sqlite3

DB_PATH = "data/fitness.db"

def connect():
    return sqlite3.connect(DB_PATH)

def setup():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT,
        category TEXT,
        sets INTEGER,
        reps INTEGER,
        weight REAL,
        notes TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()