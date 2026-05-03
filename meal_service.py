from src.models import add_meal, get_meals
from datetime import datetime


# =========================
# ADD MEAL (WITH VALIDATION)
# =========================
def create_meal(user_id, name, calories, protein, carbs, fat):
    if not name:
        return False, "Meal name required"

    try:
        calories = int(calories)
        protein = int(protein)
        carbs = int(carbs)
        fat = int(fat)
    except:
        return False, "Nutritional values must be numbers"

    if calories <= 0:
        return False, "Calories must be positive"

    success = add_meal(user_id, name, calories, protein, carbs, fat)

    if not success:
        return False, "Failed to save meal"

    return True, "Meal added successfully"


# =========================
# FETCH MEALS
# =========================
def fetch_meals(user_id):
    return get_meals(user_id)


# =========================
# DAILY SUMMARY
# =========================
def daily_summary(user_id):
    meals = get_meals(user_id)

    if not meals:
        return None, "No meals logged"

    today = datetime.now().strftime("%Y-%m-%d")

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    for m in meals:
        # assuming schema: id, user_id, name, calories, protein, carbs, fat, date
        if m[7] == today:
            total_calories += m[3]
            total_protein += m[4]
            total_carbs += m[5]
            total_fat += m[6]

    return {
        "calories": total_calories,
        "protein": total_protein,
        "carbs": total_carbs,
        "fat": total_fat
    }, None


# =========================
# MACRO ANALYSIS
# =========================
def macro_breakdown(user_id):
    meals = get_meals(user_id)

    if not meals:
        return None, "No meal data"

    protein = sum(m[4] for m in meals)
    carbs = sum(m[5] for m in meals)
    fat = sum(m[6] for m in meals)

    total = protein + carbs + fat

    if total == 0:
        return None, "No macro data"

    return {
        "protein_pct": round((protein / total) * 100, 1),
        "carbs_pct": round((carbs / total) * 100, 1),
        "fat_pct": round((fat / total) * 100, 1)
    }, None