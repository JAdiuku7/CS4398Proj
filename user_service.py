from src.models import (
    create_user,
    get_user_by_username,
    get_all_users,
    delete_user,
    toggle_user_access
)
from src.models import create_user, get_user_by_username, get_all_users, delete_user, toggle_user_access



# =========================
# REGISTER USER
# =========================
from src.models import get_user_by_username, get_all_users, delete_user, toggle_user_access
from src.auth import register_user

def register_new_user(username, password, role="user"):
    if not username or not password:
        return False, "Username and password required"

    existing = get_user_by_username(username)
    if existing:
        return False, "Username already exists"

    register_user(username, password, role)
    return True, "User created successfully"
# =========================
# FETCH USERS (ADMIN)
# =========================
def fetch_all_users():
    return get_all_users()


# =========================
# DELETE USER
# =========================
def remove_user(user_id):
    try:
        delete_user(user_id)
        return True, "User deleted"
    except:
        return False, "Error deleting user"


# =========================
# ENABLE / DISABLE USER
# =========================
def toggle_access(user_id):
    try:
        toggle_user_access(user_id)
        return True, "User access updated"
    except:
        return False, "Error updating user access"


# =========================
# CREATE TRAINER (ADMIN ONLY)
# =========================
def create_trainer(username, password):
    return register_new_user(username, password, role="trainer")


# =========================
# CREATE ADMIN (OPTIONAL)
# =========================
def create_admin(username, password):
    return register_new_user(username, password, role="admin")


# =========================
# FILTER USERS BY ROLE
# =========================
def get_users_by_role(role):
    users = get_all_users()
    return [u for u in users if u[3] == role]


# =========================
# USER SUMMARY (DASHBOARD)
# =========================
def user_summary():
    users = get_all_users()

    total = len(users)
    active = len([u for u in users if u[4] == 1])
    disabled = total - active

    roles = {
        "admins": len([u for u in users if u[3] == "admin"]),
        "trainers": len([u for u in users if u[3] == "trainer"]),
        "users": len([u for u in users if u[3] == "user"])
    }

    return {
        "total": total,
        "active": active,
        "disabled": disabled,
        "roles": roles
    }