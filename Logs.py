class ExerciseLog(Base):
    __tablename__ = "exercise_logs"
    id        = Column(Integer, primary_key=True)
    user_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    name      = Column(String(120), nullable=False)
    sets      = Column(Integer)
    reps      = Column(Integer)
    duration  = Column(Integer)  # seconds
    logged_at = Column(DateTime(timezone=True), server_default=func.now())
    user      = relationship("User", back_populates="exercise_logs")

class MealLog(Base):
    __tablename__ = "meal_logs"
    id        = Column(Integer, primary_key=True)
    user_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    name      = Column(String(120), nullable=False)
    calories  = Column(Integer)
    protein   = Column(Float)
    carbs     = Column(Float)
    fat       = Column(Float)
    logged_at = Column(DateTime(timezone=True), server_default=func.now())
    user      = relationship("User", back_populates="meal_logs")

class ProgressLog(Base):
    __tablename__ = "progress_logs"
    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    weight      = Column(Float)
    body_fat    = Column(Float)
    muscle_mass = Column(Float)
    notes       = Column(String)
    logged_at   = Column(DateTime(timezone=True), server_default=func.now())
    user        = relationship("User", back_populates="progress_logs")

class Membership(Base):
    __tablename__ = "memberships"
    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    type       = Column(String(50))
    start_date = Column(DateTime(timezone=True))
    end_date   = Column(DateTime(timezone=True))
    status     = Column(String(20), default="active")
    user       = relationship("User", back_populates="memberships")
