# models/trainer.py

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.src.base import Base

class Trainer(Base):
    __tablename__ = "trainers"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    specialization  = Column(String(120))
    certifications  = Column(String)
    bio             = Column(String)
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    user            = relationship("User", foreign_keys=[user_id])
    clients         = relationship("User", back_populates="trainer", foreign_keys="User.trainer_id")
    workout_plans   = relationship("WorkoutPlan", back_populates="trainer")
    meal_plans      = relationship("MealPlan", back_populates="trainer")