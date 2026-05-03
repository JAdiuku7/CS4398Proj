from src.database import connect
from datetime import datetime


# =========================
# USERS (ADMIN / TRAINER / USER)
# =========================
def create_user(username, password, role="user"):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (username, password, role, enabled)
        VALUES (?, ?, ?, 1)
    """, (username, password, role))

    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()

    conn.close()
    return user


def get_all_users():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    conn.close()
    return users


def delete_user(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id=?", (user_id,))

    conn.commit()
    conn.close()


def toggle_user_access(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT enabled FROM users WHERE id=?", (user_id,))
    current = cur.fetchone()[0]

    new_status = 0 if current == 1 else 1

    cur.execute("UPDATE users SET enabled=? WHERE id=?", (new_status, user_id))

    conn.commit()
    conn.close()


# =========================
# WORKOUTS
# =========================
def validate_numbers(sets, reps, weight):
    try:
        return int(sets), int(reps), float(weight)
    except:
        return None


def add_workout(user_id, exercise, category, sets, reps, weight):
    valid = validate_numbers(sets, reps, weight)
    if not valid:
        return False

    sets, reps, weight = valid

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO workouts (user_id, exercise, category, sets, reps, weight, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, exercise, category, sets, reps, weight,
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()
    conn.close()
    return True


def get_workouts(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM workouts WHERE user_id=?", (user_id,))
    data = cur.fetchall()

    conn.close()
    return data


def delete_workout(workout_id, user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM workouts WHERE id=? AND user_id=?", (workout_id, user_id))

    conn.commit()
    conn.close()


def update_workout(workout_id, user_id, exercise, sets, reps, weight):
    valid = validate_numbers(sets, reps, weight)
    if not valid:
        return False

    sets, reps, weight = valid

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        UPDATE workouts
        SET exercise=?, sets=?, reps=?, weight=?
        WHERE id=? AND user_id=?
    """, (exercise, sets, reps, weight, workout_id, user_id))

    conn.commit()
    conn.close()
    return True


# =========================
# MEALS
# =========================
def add_meal(user_id, name, calories, protein, carbs, fat):
    try:
        calories = int(calories)
        protein = int(protein)
        carbs = int(carbs)
        fat = int(fat)
    except:
        return False

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO meals (user_id, name, calories, protein, carbs, fat, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, name, calories, protein, carbs, fat,
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()
    conn.close()
    return True


def get_meals(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM meals WHERE user_id=?", (user_id,))
    data = cur.fetchall()

    conn.close()
    return data


# =========================
# GOALS
# =========================
def set_goal(user_id, target_weight, target_date):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO goals (user_id, target_weight, target_date)
        VALUES (?, ?, ?)
    """, (user_id, target_weight, target_date))

    conn.commit()
    conn.close()


def get_goals(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM goals WHERE user_id=?", (user_id,))
    data = cur.fetchall()

    conn.close()
    return data


# =========================
# TRAINER PLANS
# =========================
def assign_plan_to_user(user_id, plan_name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO plans (user_id, name)
        VALUES (?, ?)
    """, (user_id, plan_name))

    conn.commit()
    conn.close()


def get_user_plans(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM plans WHERE user_id=?", (user_id,))
    data = cur.fetchall()

    conn.close()
    return data