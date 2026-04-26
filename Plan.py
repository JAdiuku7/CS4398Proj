# models/workout_plan.py
from sqlalchemy import Column, Integer, String
from app.src.base import Base

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id              = Column(Integer, primary_key=True)
    title           = Column(String(120), nullable=False)
    description     = Column(String)
    duration_weeks  = Column(Integer)
    trainer_id      = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    user_id         = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    trainer         = relationship("Trainer", back_populates="workout_plans")
    user            = relationship("User")
    exercises       = relationship("Exercise", back_populates="workout_plan", cascade="all, delete-orphan")
    
class MealPlan(Base):
    __tablename__ = "meal_plans"

    id         = Column(Integer, primary_key=True)
    title      = Column(String(120), nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    trainer = relationship("Trainer", back_populates="meal_plans")
    user    = relationship("User")
    meals   = relationship("Meal", back_populates="meal_plan", cascade="all, delete-orphan")