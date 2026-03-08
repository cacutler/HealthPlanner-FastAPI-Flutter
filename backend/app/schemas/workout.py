from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.workout import WorkoutType, IntensityLevel
class ExerciseCreate(BaseModel):# ── Exercise schemas ──────────────────────────────────────────────────────────
    name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight_lbs: Optional[float] = None
    duration_seconds: Optional[int] = None
class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight_lbs: Optional[float] = None
    duration_seconds: Optional[int] = None
class ExerciseResponse(BaseModel):
    id: UUID
    workout_id: UUID
    name: str
    sets: Optional[int]
    reps: Optional[int]
    weight_lbs: Optional[float]
    duration_seconds: Optional[int]
    created_at: datetime
    model_config = {"from_attributes": True}
class WorkoutCreate(BaseModel):# ── Workout schemas ───────────────────────────────────────────────────────────
    type: WorkoutType
    duration_minutes: int
    intensity: IntensityLevel
    calories_burned: Optional[int] = None
    performed_at: datetime
class WorkoutUpdate(BaseModel):
    type: Optional[WorkoutType] = None
    duration_minutes: Optional[int] = None
    intensity: Optional[IntensityLevel] = None
    calories_burned: Optional[int] = None
    performed_at: Optional[datetime] = None
class WorkoutResponse(BaseModel):
    id: UUID
    user_id: UUID
    type: WorkoutType
    duration_minutes: int
    intensity: IntensityLevel
    calories_burned: Optional[int]
    performed_at: datetime
    created_at: datetime
    exercises: List[ExerciseResponse] = []
    model_config = {"from_attributes": True}