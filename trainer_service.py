from src.models import (
    assign_plan_to_user,
    get_all_users,
    get_workouts,
    get_goals,
    get_user_plans
)


# =========================
# CREATE PLAN
# =========================
def create_plan(trainer_id, plan_name):
    if not plan_name:
        return False, "Plan name required"

    # NOTE: using existing model (plans table linked to user_id)
    # If you later expand schema, this becomes trainer_id-based
    assign_plan_to_user(trainer_id, plan_name)

    return True, "Plan created"


# =========================
# ASSIGN PLAN TO USER
# =========================
def assign_plan(user_id, plan_name):
    if not user_id:
        return False, "User required"

    if not plan_name:
        return False, "Plan name required"

    assign_plan_to_user(user_id, plan_name)

    return True, "Plan assigned to user"


# =========================
# GET USERS (FOR TRAINER VIEW)
# =========================
def fetch_users():
    users = get_all_users()

    # filter only normal users
    return [u for u in users if u[3] == "user"]


# =========================
# VIEW USER PROGRESS
# =========================
def user_progress(user_id):
    workouts = get_workouts(user_id)
    goals = get_goals(user_id)

    if not workouts:
        return None, "No workout data"

    latest_workout = workouts[-1]

    progress_data = {
        "latest_exercise": latest_workout[2],
        "latest_weight": latest_workout[6],
        "total_sessions": len(workouts)
    }

    # include goal if exists
    if goals:
        goal = goals[-1]
        progress_data["target_weight"] = goal[2]
        progress_data["goal_date"] = goal[3]

    return progress_data, None


# =========================
# VIEW ASSIGNED PLANS
# =========================
def fetch_user_plans(user_id):
    return get_user_plans(user_id)


# =========================
# DASHBOARD SUMMARY (TRAINER)
# =========================
def trainer_dashboard():
    users = fetch_users()

    total_users = len(users)

    active_users = len([u for u in users if u[4] == 1])  # enabled

    return {
        "total_users": total_users,
        "active_users": active_users
    }