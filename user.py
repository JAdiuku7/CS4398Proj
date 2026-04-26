import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.src.base import Base


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    TRAINER = "trainer"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.USER)
    is_active = Column(Boolean, nullable=False, default=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    trainer = relationship("Trainer", back_populates="clients", foreign_keys=[trainer_id])
    trainer_profile = relationship(
        "Trainer",
        back_populates="user",
        foreign_keys="Trainer.user_id",
        uselist=False,
    )
    exercise_logs = relationship(
        "ExerciseLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} role={self.role}>"


class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    specialization = Column(String(120), nullable=True)
    certifications = Column(String(255), nullable=True)
    bio = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="trainer_profile", foreign_keys=[user_id])
    clients = relationship("User", back_populates="trainer", foreign_keys="User.trainer_id")

    def __repr__(self) -> str:
        return f"<Trainer id={self.id} user_id={self.user_id}>"