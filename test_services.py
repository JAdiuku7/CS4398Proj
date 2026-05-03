import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Make project root importable when running tests from the repo root
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import services.user_service as user_service
import services.workout_service as workout_service
import services.meal_service as meal_service
import services.goal_service as goal_service
import services.trainer_service as trainer_service


class TestUserService(unittest.TestCase):
    def test_register_new_user_fails_when_fields_missing(self):
        success, msg = user_service.register_new_user("", "")
        self.assertFalse(success)
        self.assertIn("required", msg.lower())

    def test_register_new_user_fails_on_duplicate_username(self):
        with patch.object(user_service, "get_user_by_username", return_value=(1, "alex", "hash", "user", 1)):
            success, msg = user_service.register_new_user("alex", "password123")
            self.assertFalse(success)
            self.assertIn("exists", msg.lower())

    def test_register_new_user_success(self):
        with patch.object(user_service, "get_user_by_username", return_value=None), \
         patch.object(user_service, "register_user") as register_mock:
            success, msg = user_service.register_new_user("alex", "password123", "user")

        self.assertTrue(success)
        self.assertIn("created", msg.lower())
        register_mock.assert_called_once_with("alex", "password123", "user")

    def test_fetch_all_users(self):
        sample_users = [
            (1, "admin1", "hash", "admin", 1),
            (2, "trainer1", "hash", "trainer", 1),
        ]
        with patch.object(user_service, "get_all_users", return_value=sample_users):
            users = user_service.fetch_all_users()
            self.assertEqual(len(users), 2)

    def test_toggle_access(self):
        with patch.object(user_service, "toggle_user_access") as toggle_mock:
            success, msg = user_service.toggle_access(10)
            self.assertTrue(success)
            self.assertIn("updated", msg.lower())
            toggle_mock.assert_called_once_with(10)

    def test_remove_user(self):
        with patch.object(user_service, "delete_user") as delete_mock:
            success, msg = user_service.remove_user(5)
            self.assertTrue(success)
            self.assertIn("deleted", msg.lower())
            delete_mock.assert_called_once_with(5)

    def test_user_summary(self):
        sample_users = [
            (1, "admin1", "hash", "admin", 1),
            (2, "trainer1", "hash", "trainer", 1),
            (3, "user1", "hash", "user", 0),
        ]
        with patch.object(user_service, "get_all_users", return_value=sample_users):
            summary = user_service.user_summary()
            self.assertEqual(summary["total"], 3)
            self.assertEqual(summary["active"], 2)
            self.assertEqual(summary["disabled"], 1)
            self.assertEqual(summary["roles"]["admins"], 1)
            self.assertEqual(summary["roles"]["trainers"], 1)
            self.assertEqual(summary["roles"]["users"], 1)


class TestWorkoutService(unittest.TestCase):
    def test_create_workout_rejects_missing_exercise(self):
        success, msg = workout_service.create_workout(1, "", "Push", 3, 10, 100)
        self.assertFalse(success)
        self.assertIn("exercise", msg.lower())

    def test_create_workout_rejects_invalid_numbers(self):
        success, msg = workout_service.create_workout(1, "Bench Press", "Push", "x", 10, 100)
        self.assertFalse(success)
        self.assertIn("numbers", msg.lower())

    def test_create_workout_success(self):
        with patch.object(workout_service, "add_workout", return_value=True) as add_mock:
            success, msg = workout_service.create_workout(1, "Bench Press", "Push", 3, 10, 100)
            self.assertTrue(success)
            self.assertIn("added", msg.lower())
            add_mock.assert_called_once()

    def test_fetch_workouts(self):
        sample = [
            (1, 1, "Bench Press", "Push", 3, 10, 100, "2026-05-03"),
        ]
        with patch.object(workout_service, "get_workouts", return_value=sample):
            workouts = workout_service.fetch_workouts(1)
            self.assertEqual(len(workouts), 1)

    def test_edit_workout_success(self):
        with patch.object(workout_service, "update_workout", return_value=True) as update_mock:
            success, msg = workout_service.edit_workout(7, 1, "Squat", 5, 5, 185)
            self.assertTrue(success)
            self.assertIn("updated", msg.lower())
            update_mock.assert_called_once()

    def test_remove_workout(self):
        with patch.object(workout_service, "delete_workout") as delete_mock:
            success, msg = workout_service.remove_workout(7, 1)
            self.assertTrue(success)
            self.assertIn("deleted", msg.lower())
            delete_mock.assert_called_once_with(7, 1)

    def test_calculate_volume(self):
        sample = [
            (1, 1, "Bench Press", "Push", 3, 10, 100, "2026-05-03"),
            (2, 1, "Squat", "Legs", 5, 5, 185, "2026-05-03"),
        ]
        with patch.object(workout_service, "get_workouts", return_value=sample):
            volume = workout_service.calculate_volume(1)
            expected = (3 * 10 * 100) + (5 * 5 * 185)
            self.assertEqual(volume, expected)

    def test_get_prs(self):
        sample = [
            (1, 1, "Bench Press", "Push", 3, 10, 100, "2026-05-03"),
            (2, 1, "Bench Press", "Push", 5, 5, 120, "2026-05-04"),
            (3, 1, "Squat", "Legs", 5, 5, 185, "2026-05-03"),
        ]
        with patch.object(workout_service, "get_workouts", return_value=sample):
            prs = workout_service.get_prs(1)
            self.assertEqual(prs["Bench Press"], 120)
            self.assertEqual(prs["Squat"], 185)

    def test_build_chart_data(self):
        sample = [
            (1, 1, "Bench Press", "Push", 3, 10, 100, "2026-05-03"),
            (2, 1, "Bench Press", "Push", 5, 5, 120, "2026-05-04"),
        ]
        with patch.object(workout_service, "get_workouts", return_value=sample):
            chart_data = workout_service.build_chart_data(1)
            self.assertIn("Bench Press", chart_data)
            self.assertEqual(chart_data["Bench Press"]["dates"], ["2026-05-03", "2026-05-04"])
            self.assertEqual(chart_data["Bench Press"]["weights"], [100, 120])


class TestMealService(unittest.TestCase):
    def test_create_meal_rejects_empty_name(self):
        success, msg = meal_service.create_meal(1, "", 500, 30, 40, 20)
        self.assertFalse(success)
        self.assertIn("required", msg.lower())

    def test_create_meal_rejects_bad_numbers(self):
        success, msg = meal_service.create_meal(1, "Chicken Bowl", "abc", 30, 40, 20)
        self.assertFalse(success)
        self.assertIn("numbers", msg.lower())

    def test_create_meal_success(self):
        with patch.object(meal_service, "add_meal", return_value=True) as add_mock:
            success, msg = meal_service.create_meal(1, "Chicken Bowl", 500, 30, 40, 20)
            self.assertTrue(success)
            self.assertIn("success", msg.lower())
            add_mock.assert_called_once()

    def test_fetch_meals(self):
        sample = [
            (1, 1, "Chicken Bowl", 500, 30, 40, 20, "2026-05-03"),
        ]
        with patch.object(meal_service, "get_meals", return_value=sample):
            meals = meal_service.fetch_meals(1)
            self.assertEqual(len(meals), 1)

    def test_daily_summary(self):
        sample = [
            (1, 1, "Chicken Bowl", 500, 30, 40, 20, "2026-05-03"),
            (2, 1, "Shake", 250, 25, 20, 5, "2026-05-03"),
            (3, 1, "Old Meal", 700, 40, 60, 20, "2026-05-02"),
        ]
        fake_datetime = MagicMock()
        fake_now = MagicMock()
        fake_now.strftime.return_value = "2026-05-03"
        fake_datetime.now.return_value = fake_now

        with patch.object(meal_service, "get_meals", return_value=sample), \
             patch.object(meal_service, "datetime", fake_datetime):
            summary, error = meal_service.daily_summary(1)
            self.assertIsNone(error)
            self.assertEqual(summary["calories"], 750)
            self.assertEqual(summary["protein"], 55)
            self.assertEqual(summary["carbs"], 60)
            self.assertEqual(summary["fat"], 25)

    def test_macro_breakdown(self):
        sample = [
            (1, 1, "Chicken Bowl", 500, 30, 40, 20, "2026-05-03"),
            (2, 1, "Shake", 250, 25, 20, 5, "2026-05-03"),
        ]
        with patch.object(meal_service, "get_meals", return_value=sample):
            macros, error = meal_service.macro_breakdown(1)
            self.assertIsNone(error)
            self.assertIn("protein_pct", macros)
            self.assertIn("carbs_pct", macros)
            self.assertIn("fat_pct", macros)


class TestGoalService(unittest.TestCase):
    def test_create_goal_rejects_bad_weight(self):
        success, msg = goal_service.create_goal(1, "abc", "2026-06-01")
        self.assertFalse(success)
        self.assertIn("invalid weight", msg.lower())

    def test_create_goal_rejects_bad_date(self):
        success, msg = goal_service.create_goal(1, "180", "06/01/2026")
        self.assertFalse(success)
        self.assertIn("date", msg.lower())

    def test_create_goal_success(self):
        with patch.object(goal_service, "set_goal") as set_goal_mock:
            success, msg = goal_service.create_goal(1, "180", "2026-06-01")
            self.assertTrue(success)
            self.assertIn("created", msg.lower())
            set_goal_mock.assert_called_once_with(1, 180.0, "2026-06-01")

    def test_fetch_goals(self):
        sample = [
            (1, 1, 180.0, "2026-06-01"),
        ]
        with patch.object(goal_service, "get_goals", return_value=sample):
            goals = goal_service.fetch_goals(1)
            self.assertEqual(len(goals), 1)

    def test_goal_summary(self):
        workouts = [
            (1, 1, "Bench Press", "Push", 3, 10, 185, "2026-05-03"),
        ]
        goals = [
            (1, 1, 180.0, "2026-06-01"),
        ]
        with patch.object(goal_service, "get_workouts", return_value=workouts), \
             patch.object(goal_service, "get_goals", return_value=goals):
            summary = goal_service.goal_summary(1)
            self.assertEqual(summary["current"], 185)
            self.assertEqual(summary["target"], 180.0)
            self.assertIn("goal", summary["status"].lower())


class TestTrainerService(unittest.TestCase):
    def test_create_plan(self):
        with patch.object(trainer_service, "assign_plan_to_user") as assign_mock:
            success, msg = trainer_service.create_plan(2, "Push Day Plan")
            self.assertTrue(success)
            self.assertIn("created", msg.lower())
            assign_mock.assert_called_once_with(2, "Push Day Plan")

    def test_assign_plan(self):
        with patch.object(trainer_service, "assign_plan_to_user") as assign_mock:
            success, msg = trainer_service.assign_plan(5, "Meal Plan A")
            self.assertTrue(success)
            self.assertIn("assigned", msg.lower())
            assign_mock.assert_called_once_with(5, "Meal Plan A")

    def test_fetch_users_filters_only_users(self):
        sample_users = [
            (1, "admin1", "hash", "admin", 1),
            (2, "trainer1", "hash", "trainer", 1),
            (3, "user1", "hash", "user", 1),
        ]
        with patch.object(trainer_service, "get_all_users", return_value=sample_users):
            users = trainer_service.fetch_users()
            self.assertEqual(len(users), 1)
            self.assertEqual(users[0][1], "user1")

    def test_user_progress(self):
        workouts = [
            (1, 3, "Bench Press", "Push", 3, 10, 185, "2026-05-03"),
        ]
        goals = [
            (1, 3, 180.0, "2026-06-01"),
        ]
        with patch.object(trainer_service, "get_workouts", return_value=workouts), \
             patch.object(trainer_service, "get_goals", return_value=goals):
            progress, error = trainer_service.user_progress(3)
            self.assertIsNone(error)
            self.assertEqual(progress["latest_exercise"], "Bench Press")
            self.assertEqual(progress["latest_weight"], 185)
            self.assertEqual(progress["total_sessions"], 1)
            self.assertEqual(progress["target_weight"], 180.0)

    def test_trainer_dashboard(self):
        sample_users = [
            (1, "user1", "hash", "user", 1),
            (2, "user2", "hash", "user", 0),
            (3, "trainer1", "hash", "trainer", 1),
        ]
        with patch.object(trainer_service, "fetch_users", return_value=sample_users):
            summary = trainer_service.trainer_dashboard()
            self.assertEqual(summary["total_users"], 3)
            self.assertEqual(summary["active_users"], 2)


if __name__ == "__main__":
    unittest.main()