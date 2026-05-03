from modules.database import connect

def get_prs():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT exercise, MAX(weight)
    FROM workouts
    GROUP BY exercise
    """)

    results = cur.fetchall()
    conn.close()

    return results