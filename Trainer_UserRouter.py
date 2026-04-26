from fastapi import APIRouter, Depends
from pydantic import BaseModel

class WorkoutPlanResponse(BaseModel):
    id: int
    name: str
    email: str

class MealPlanResponse(BaseModel):
    id: int
    name: str
    email: str

class LogResponse(BaseModel):
    pass
class GoalResponse(BaseModel):
    pass

trainer_router = APIRouter(prefix="/api/trainer", tags=["trainer"])

@trainer_router.post("/workout-plans", response_model=WorkoutPlanResponse)
def create_workout_plan():
    pass

@trainer_router.post("/meal-plans", response_model=MealPlanResponse)
def create_meal_plan():
    pass

@trainer_router.patch("/workout-plans/{id}/assign")
def assign_workout_plan(id: int):
    pass

@trainer_router.get("/clients/{id}/progress")
def get_client_progress(id: int):
    pass


# USER ROUTES
user_router = APIRouter(prefix="/api/user", tags=["user"])

@user_router.post("/exercises", response_model=LogResponse, status_code=201)
def log_exercise():
    pass

@user_router.post("/meals", response_model=LogResponse, status_code=201)
def log_meal():
    pass

@user_router.post("/progress", response_model=LogResponse, status_code=201)
def log_progress():
    pass

@user_router.post("/goals", response_model=GoalResponse, status_code=201)
def create_goal():
    pass

@user_router.get("/dashboard")
def get_dashboard():
    pass