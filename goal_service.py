from src.models import set_goal, get_goals, get_workouts
from datetime import datetime
from src.models import add_goal, get_goals, add_weight_log, get_weight_logs

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

    latest_workout = workouts[-1]
    current_weight = latest_workout[6]

    latest_goal = goals[-1]

    # Support both schema styles:
    # old test style: (id, user_id, target_weight, target_date)
    # new style: (id, user_id, current_weight, goal_weight, target_date, created_at)
    if len(latest_goal) >= 4 and isinstance(latest_goal[3], (int, float)):
        target_weight = latest_goal[3]
    else:
        target_weight = latest_goal[2]

    return {
        "current_weight": float(current_weight),
        "target_weight": float(target_weight),
        "difference": float(current_weight) - float(target_weight)
    }, None

# =========================
# GOAL SUMMARY (for dashboard)
# =========================
def goal_summary(user_id):
    progress, error = calculate_progress(user_id)

    if error:
        return {
            "current_weight": None,
            "goal_weight": None,
            "status": error
        }

    # progress already gives current_weight and target_weight as numeric values
    current_weight = progress["current_weight"]
    target_weight = progress["target_weight"]

    try:
        current_weight = float(current_weight)
        target_weight = float(target_weight)
    except (TypeError, ValueError):
        return {
            "current_weight": current_weight,
            "goal_weight": target_weight,
            "status": "Invalid goal data"
        }

    diff = current_weight - target_weight

    if diff <= 0:
        status = "Goal reached or below target"
    else:
        status = f"{round(diff, 1)} away from target"

    return {
        "current_weight": current_weight,
        "goal_weight": target_weight,
        "status": status
    }


def save_weight_and_goal(user_id, current_weight, goal_weight, target_date):
    try:
        current_weight = float(current_weight)
        goal_weight = float(goal_weight)
    except:
        return False, "Current weight and goal weight must be numbers"

    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except:
        return False, "Invalid date format"

    add_weight_log(user_id, current_weight)
    add_goal(user_id, current_weight, goal_weight, target_date)
    return True, "Goal and weight saved"


def fetch_goals(user_id):
    return get_goals(user_id)


def fetch_weight_logs(user_id):
    return get_weight_logs(user_id)


def weight_chart_data(user_id):
    goals = get_goals(user_id)

    # goals rows should be:
    # id, user_id, current_weight, goal_weight, target_date, created_at
    dates = []
    weights = []

    for g in goals:
        dates.append(g[4])      # target_date
        weights.append(g[2])    # current_weight

    return {
        "dates": dates,
        "weights": weights
    }
