import uuid
import enum
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
class WorkoutType(str, enum.Enum):
    strength = "strength"  # Fixed: was strenght = "strength" (key typo)
    cardio = "cardio"
class IntensityLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
class Workout(Base):
    __tablename__ = "workouts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(Enum(WorkoutType), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    intensity = Column(Enum(IntensityLevel), nullable=False)
    calories_burned = Column(Integer)
    performed_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout", cascade="all, delete-orphan")