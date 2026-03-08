from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Sequence
from uuid import UUID
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.workout import Workout
from app.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutResponse
router = APIRouter(prefix="/workouts", tags=["workouts"])
@router.get("", response_model=list[WorkoutResponse])
async def list_workouts(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> Sequence[Workout]:
    result = await db.execute(select(Workout).where(Workout.user_id == current_user.id).options(selectinload(Workout.exercises)).order_by(Workout.performed_at.desc()))
    return result.scalars().all()
@router.post("", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def create_workout(body: WorkoutCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> Workout:
    workout = Workout(**body.model_dump(), user_id=current_user.id)
    db.add(workout)
    await db.commit()
    await db.refresh(workout)
    result = await db.execute(select(Workout).where(Workout.id == workout.id).options(selectinload(Workout.exercises)))# Reload with exercises relationship
    return result.scalar_one()
@router.get("/{workout_id}", response_model=WorkoutResponse)
async def get_workout(workout_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> Workout:
    result = await db.execute(select(Workout).where(Workout.id == workout_id, Workout.user_id == current_user.id).options(selectinload(Workout.exercises)))
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout
@router.patch("/{workout_id}", response_model=WorkoutResponse)
async def update_workout(workout_id: UUID, body: WorkoutUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> Workout:
    result = await db.execute(select(Workout).where(Workout.id == workout_id, Workout.user_id == current_user.id).options(selectinload(Workout.exercises)))
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(workout, field, value)
    await db.commit()
    await db.refresh(workout)
    return workout
@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(workout_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> None:
    result = await db.execute(select(Workout).where(Workout.id == workout_id, Workout.user_id == current_user.id))
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    await db.delete(workout)
    await db.commit()