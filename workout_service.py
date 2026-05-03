from src.models import (
    add_workout,
    get_workouts,
    update_workout,
    delete_workout
)


# =========================
# CREATE WORKOUT
# =========================
def create_workout(user_id, exercise, category, sets, reps, weight):
    if not exercise:
        return False, "Exercise required"

    try:
        sets = int(sets)
        reps = int(reps)
        weight = float(weight)
    except:
        return False, "Sets/Reps/Weight must be numbers"

    if sets <= 0 or reps <= 0 or weight < 0:
        return False, "Invalid values"

    success = add_workout(user_id, exercise, category, sets, reps, weight)

    if not success:
        return False, "Failed to save workout"

    return True, "Workout added"


# =========================
# FETCH WORKOUTS
# =========================
def fetch_workouts(user_id):
    return get_workouts(user_id)


# =========================
# UPDATE WORKOUT
# =========================
def edit_workout(workout_id, user_id, exercise, sets, reps, weight):
    try:
        sets = int(sets)
        reps = int(reps)
        weight = float(weight)
    except:
        return False, "Invalid input"

    success = update_workout(workout_id, user_id, exercise, sets, reps, weight)

    if not success:
        return False, "Update failed"

    return True, "Workout updated"


# =========================
# DELETE WORKOUT
# =========================
def remove_workout(workout_id, user_id):
    try:
        delete_workout(workout_id, user_id)
        return True, "Workout deleted"
    except:
        return False, "Error deleting workout"


# =========================
# VOLUME CALCULATION
# =========================
def calculate_volume(user_id):
    workouts = get_workouts(user_id)

    if not workouts:
        return 0

    total = 0

    for w in workouts:
        # sets * reps * weight
        total += w[4] * w[5] * w[6]

    return total


# =========================
# PERSONAL RECORDS (PRs)
# =========================
def get_prs(user_id):
    workouts = get_workouts(user_id)

    prs = {}

    for w in workouts:
        ex = w[2]
        weight = w[6]

        if ex not in prs or weight > prs[ex]:
            prs[ex] = weight

    return prs


# =========================
# CHART DATA (PER EXERCISE)
# =========================
def build_chart_data(user_id):
    workouts = get_workouts(user_id)

    data = {}

    for w in workouts:
        ex = w[2]

        if ex not in data:
            data[ex] = {"dates": [], "weights": []}

        data[ex]["dates"].append(w[7])
        data[ex]["weights"].append(w[6])

    return data