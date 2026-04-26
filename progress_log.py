# models/progress_log.py
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