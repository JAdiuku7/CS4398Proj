from flask import Flask, render_template, request, redirect, session, flash
import json

from src.database import setup_db
from src.auth import login_user

from services.user_service import (
    register_new_user,
    fetch_all_users,
    remove_user,
    toggle_access,
)
from services.workout_service import (
    create_workout,
    fetch_workouts,
    edit_workout,
    remove_workout,
    build_chart_data,
)
from services.meal_service import create_meal, fetch_meals, daily_summary
from services.goal_service import create_goal, fetch_goals, goal_summary
from services.trainer_service import fetch_users, assign_plan, fetch_user_plans
from services.goal_service import save_weight_and_goal, fetch_goals, goal_summary, weight_chart_data
from services.workout_service import calculate_volume, get_prs, build_chart_data
from services.goal_service import weight_chart_data


app = Flask(__name__)
app.secret_key = "supersecretkey"

setup_db()


# =========================
# HELPERS
# =========================
def login_required():
    if "user_id" not in session:
        return redirect("/login")
    return None


def admin_required():
    if session.get("role") != "admin":
        return redirect("/dashboard")
    return None


def trainer_required():
    if session.get("role") != "trainer":
        return redirect("/dashboard")
    return None


# =========================
# AUTH ROUTES
# =========================
@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = login_user(request.form["username"], request.form["password"])

        if user:
            session["user_id"] = user[0]
            session["role"] = user[3]
            flash("Logged in successfully.")
            return redirect("/dashboard")

        flash("Invalid login")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        success, msg = register_new_user(
            request.form["username"],
            request.form["password"],
            "user",
        )
        flash(msg)
        if success:
            return redirect("/login")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    workout_chart = build_chart_data(session["user_id"])
    weight_chart = weight_chart_data(session["user_id"])
    goals = fetch_goals(session["user_id"])
    summary = goal_summary(session["user_id"])
    workouts = fetch_workouts(session["user_id"])
    meals = fetch_meals(session["user_id"])

    total_workouts = len(workouts)
    unique_exercises = len(set(w[2] for w in workouts)) if workouts else 0
    print("WEIGHT CHART:", weight_chart)
    return render_template(
        "dashboard.html",
        workouts=workouts,
        meals=meals,
        goals=goals,
        workout_chart=workout_chart,
        weight_chart=weight_chart,
        summary=summary,
        total_workouts=total_workouts,
        unique_exercises=unique_exercises,
        goal_info=summary
    )


# =========================
# WORKOUTS
# =========================
@app.route("/workouts")
def workouts_page():
    redirect_response = login_required()
    if redirect_response:
        return redirect_response

    workouts = fetch_workouts(session["user_id"])
    return render_template("workouts.html", workouts=workouts)


@app.route("/add", methods=["POST"])
def add():
    redirect_response = login_required()
    if redirect_response:
        return redirect_response

    success, msg = create_workout(
        session["user_id"],
        request.form["exercise"],
        request.form["category"],
        request.form["sets"],
        request.form["reps"],
        request.form["weight"],
    )
    flash(msg)
    return redirect("/dashboard")


@app.route("/update", methods=["POST"])
def update():
    redirect_response = login_required()
    if redirect_response:
        return redirect_response

    success, msg = edit_workout(
        request.form["id"],
        session["user_id"],
        request.form["exercise"],
        request.form["sets"],
        request.form["reps"],
        request.form["weight"],
    )
    flash(msg)
    return redirect("/workouts")


@app.route("/delete/<int:workout_id>")
def delete(workout_id):
    redirect_response = login_required()
    if redirect_response:
        return redirect_response

    success, msg = remove_workout(workout_id, session["user_id"])
    flash(msg)
    return redirect("/workouts")


# =========================
# MEALS
# =========================
@app.route("/meals", methods=["GET", "POST"])
def meals():
    redirect_response = login_required()
    if redirect_response:
        return redirect_response

    if request.method == "POST":
        success, msg = create_meal(
            session["user_id"],
            request.form["name"],
            request.form["calories"],
            request.form["protein"],
            request.form["carbs"],
            request.form["fat"],
        )
        flash(msg)

    meals_list = fetch_meals(session["user_id"])
    summary, _ = daily_summary(session["user_id"])

    return render_template("meals.html", meals=meals_list, summary=summary)


# =========================
# GOALS
# =========================


@app.route("/goals", methods=["GET", "POST"])
def goals():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        success, msg = save_weight_and_goal(
            session["user_id"],
            request.form["current_weight"],
            request.form["goal_weight"],
            request.form["target_date"]
        )
        flash(msg)

    goals_list = fetch_goals(session["user_id"])
    summary = goal_summary(session["user_id"])
    chart = weight_chart_data(session["user_id"])

    return render_template("goals.html", goals=goals_list, summary=summary, chart=json.dumps(chart))

# =========================
# ANALYTICS
# =========================


@app.route("/analytics")
def analytics():
    if "user_id" not in session:
        return redirect("/login")

    workout_chart = build_chart_data(session["user_id"])
    weight_data = weight_chart_data(session["user_id"])
    volume = calculate_volume(session["user_id"])
    prs = get_prs(session["user_id"])
    workouts = fetch_workouts(session["user_id"])

    return render_template(
        "analytics.html",
        workout_chart=json.dumps(workout_chart),
        weight_chart = weight_chart_data(session["user_id"]),
        #weight_chart=json.dumps(weight_data),
        volume=volume,
        prs=prs,
        workouts=workouts
    )


# =========================
# ADMIN PANEL
# =========================
@app.route("/admin")
def admin():
    redirect_response = login_required()
    if redirect_response:
        return redirect_response

    role_response = admin_required()
    if role_response:
        return role_response

    users = fetch_all_users()
    return render_template("admin.html", users=users)


@app.route("/admin/toggle/<int:user_id>")
def toggle_user(user_id):
    redirect_response = login_required()
    if redirect_response:
        return redirect_response

    role_response = admin_required()
    if role_response:
        return role_response

    success, msg = toggle_access(user_id)
    flash(msg)
    return redirect("/admin")


@app.route("/admin/delete/<int:user_id>")
def delete_user_route(user_id):
    redirect_response = login_required()
    if redirect_response:
        return redirect_response

    role_response = admin_required()
    if role_response:
        return role_response

    success, msg = remove_user(user_id)
    flash(msg)
    return redirect("/admin")


# =========================
# TRAINER PANEL
# =========================
@app.route("/trainer", methods=["GET", "POST"])
def trainer():
    redirect_response = login_required()
    if redirect_response:
        return redirect_response

    role_response = trainer_required()
    if role_response:
        return role_response

    if request.method == "POST":
        success, msg = assign_plan(
            request.form["user_id"],
            request.form["plan_name"],
        )
        flash(msg)

    users = fetch_users()

    assigned_plans = []
    for u in users:
        plans = fetch_user_plans(u[0])
        for plan in plans:
            assigned_plans.append((u[1], plan[0], plan[2], plan[3]))

    return render_template(
        "trainer.html",
        users=users,
        assigned_plans=assigned_plans,
    )


if __name__ == "__main__":
    app.run(debug=True)