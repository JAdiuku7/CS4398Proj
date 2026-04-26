import enum

from sqlalchemy import (
    CheckConstraint, Column, DateTime,
    Enum, Float, ForeignKey, Integer, String, Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.src.base import Base


class MuscleGroup(str, enum.Enum):
    CHEST = "chest"
    BACK = "back"
    SHOULDERS = "shoulders"
    ARMS = "arms"
    LEGS = "legs"
    CORE = "core"
    FULL_BODY = "full_body"
    CARDIO = "cardio"
    OTHER = "other"


class DifficultyLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ExerciseLog(Base):
    __tablename__ = "exercise_logs"

    __table_args__ = (
        CheckConstraint("sets >= 1", name="ck_sets_positive"),
        CheckConstraint("reps >= 1", name="ck_reps_positive"),
        CheckConstraint("weight_kg >= 0", name="ck_weight_non_negative"),
        CheckConstraint("duration_secs >= 1", name="ck_duration_positive"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    exercise_name = Column(String(120), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight_kg = Column(Float, nullable=False, default=0.0)

    duration_secs = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    muscle_group = Column(Enum(MuscleGroup), nullable=True)
    difficulty = Column(Enum(DifficultyLevel), nullable=True)

    logged_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="exercise_logs")

    def __repr__(self) -> str:
        return (
            f"<ExerciseLog id={self.id} user={self.user_id} "
            f"name={self.exercise_name!r} {self.sets}x{self.reps} @ {self.weight_kg}kg>"
        )