import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workout_id = Column(UUID(as_uuid=True), ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight_lbs = Column(Numeric(5, 2))
    duration_seconds = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Fixed: was create_at
    workout = relationship("Workout", back_populates="exercises")