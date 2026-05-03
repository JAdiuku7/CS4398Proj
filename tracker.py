from modules.database import connect
from datetime import datetime

def validate(sets, reps, weight):
    try:
        return int(sets), int(reps), float(weight)
    except:
        return None

def add_workout(exercise, category, sets, reps, weight, notes):
    valid = validate(sets, reps, weight)
    if not valid:
        return False

    sets, reps, weight = valid

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO workouts (exercise, category, sets, reps, weight, notes, date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (exercise, category, sets, reps, weight, notes,
          datetime.now().strftime("%Y-%m-%d %H:%M")))

    conn.commit()
    conn.close()
    return True

def get_workouts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM workouts")
    rows = cur.fetchall()

    conn.close()
    return rows

def delete_workout(workout_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM workouts WHERE id=?", (workout_id,))
    conn.commit()
    conn.close()

def update_workout(workout_id, exercise, category, sets, reps, weight, notes):
    valid = validate(sets, reps, weight)
    if not valid:
        return False

    sets, reps, weight = valid

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE workouts
    SET exercise=?, category=?, sets=?, reps=?, weight=?, notes=?
    WHERE id=?
    """, (exercise, category, sets, reps, weight, notes, workout_id))

    conn.commit()
    conn.close()
    return True