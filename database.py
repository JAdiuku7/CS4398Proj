import sqlite3

DB = "data/fitness.db"


def connect():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = 1")
    return conn


def setup_db():
    conn = connect()
    cur = conn.cursor()

    # =========================
    # USERS (Admin / Trainer / User)
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,              -- 'admin', 'trainer', 'user'
        enabled INTEGER DEFAULT 1
    )
    """)

    # =========================
    # WORKOUTS
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        exercise TEXT,
        category TEXT,
        sets INTEGER,
        reps INTEGER,
        weight REAL,
        date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # =========================
    # MEALS
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        calories INTEGER,
        protein INTEGER,
        carbs INTEGER,
        fat INTEGER,
        date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # =========================
    # GOALS
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        target_weight REAL,
        target_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # =========================
    # TRAINER PLANS
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # =========================
    # OPTIONAL: PAYMENTS / MEMBERSHIPS (SRS requirement)
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS memberships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        start_date TEXT,
        end_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        date TEXT,
        status TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()