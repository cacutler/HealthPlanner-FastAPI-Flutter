from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence
from uuid import UUID
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.workout import Workout
from app.models.exercise import Exercise
from app.schemas.workout import ExerciseCreate, ExerciseUpdate, ExerciseResponse
router = APIRouter(prefix="/workouts/{workout_id}/exercises", tags=["exercises"])
async def _get_workout_or_404(workout_id: UUID, user_id: UUID, db: AsyncSession) -> Workout:
    result = await db.execute(select(Workout).where(Workout.id == workout_id, Workout.user_id == user_id))
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout
@router.get("", response_model=list[ExerciseResponse])
async def list_exercises(workout_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> Sequence[Exercise]:
    await _get_workout_or_404(workout_id, current_user.id, db)
    result = await db.execute(select(Exercise).where(Exercise.workout_id == workout_id))
    return result.scalars().all()
@router.post("", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def add_exercise(workout_id: UUID, body: ExerciseCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> Exercise:
    await _get_workout_or_404(workout_id, current_user.id, db)
    exercise = Exercise(**body.model_dump(), workout_id=workout_id)
    db.add(exercise)
    await db.commit()
    await db.refresh(exercise)
    return exercise
@router.patch("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(workout_id: UUID, exercise_id: UUID, body: ExerciseUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> Exercise:
    await _get_workout_or_404(workout_id, current_user.id, db)
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id, Exercise.workout_id == workout_id))
    exercise = result.scalar_one_or_none()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(exercise, field, value)
    await db.commit()
    await db.refresh(exercise)
    return exercise
@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(workout_id: UUID, exercise_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> None:
    await _get_workout_or_404(workout_id, current_user.id, db)
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id, Exercise.workout_id == workout_id))
    exercise = result.scalar_one_or_none()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    await db.delete(exercise)
    await db.commit()