from src.models import set_goal, get_goals, get_workouts
from datetime import datetime


# =========================
# CREATE GOAL
# =========================
def create_goal(user_id, target_weight, target_date):
    # validation
    try:
        target_weight = float(target_weight)
    except:
        return False, "Invalid weight"

    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except:
        return False, "Invalid date format (YYYY-MM-DD)"

    set_goal(user_id, target_weight, target_date)
    return True, "Goal created"


# =========================
# GET USER GOALS
# =========================
def fetch_goals(user_id):
    return get_goals(user_id)


# =========================
# PROGRESS ANALYSIS
# =========================
def calculate_progress(user_id):
    workouts = get_workouts(user_id)
    goals = get_goals(user_id)

    if not workouts:
        return None, "No workout data"

    if not goals:
        return None, "No goals set"

    # latest goal
    goal = goals[-1]
    target_weight = goal[2]

    # latest workout weight (simple metric)
    latest_weight = workouts[-1][6]

    progress = latest_weight - target_weight

    return {
        "current_weight": latest_weight,
        "target_weight": target_weight,
        "difference": progress
    }, None


# =========================
# GOAL SUMMARY (for dashboard)
# =========================
def goal_summary(user_id):
    progress, error = calculate_progress(user_id)

    if error:
        return {
            "status": "No data",
            "message": error
        }

    diff = progress["difference"]

    if diff >= 0:
        status = "Goal reached or exceeded 🎉"
    else:
        status = f"{abs(diff)} away from goal"

    return {
        "current": progress["current_weight"],
        "target": progress["target_weight"],
        "status": status
    }