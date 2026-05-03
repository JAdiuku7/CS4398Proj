from src.database import connect
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username, password, role="user"):
    conn = connect()
    cur = conn.cursor()

    hashed = generate_password_hash(password)

    cur.execute(
        "INSERT INTO users (username, password, role, enabled) VALUES (?, ?, ?, 1)",
        (username, hashed, role)
    )

    conn.commit()
    conn.close()


def login_user(username, password):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()

    if user and user[4] == 1:
        if check_password_hash(user[2], password):
            return user

    return None