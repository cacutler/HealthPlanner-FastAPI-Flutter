from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import Sequence
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.nutrition import NutritionLog
from app.schemas.nutrition_weight import NutritionCreate, NutritionUpdate, NutritionResponse
router = APIRouter(prefix="/nutrition", tags=["nutrition"])
@router.get("", response_model=list[NutritionResponse])
async def list_nutrition(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user),) -> Sequence[NutritionLog]:
    result = await db.execute(select(NutritionLog).where(NutritionLog.user_id == current_user.id).order_by(NutritionLog.logged_at.desc()))
    return result.scalars().all()
@router.post("", response_model=NutritionResponse, status_code=status.HTTP_201_CREATED)
async def log_nutrition(
    body: NutritionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)) -> NutritionLog:
    entry = NutritionLog(**body.model_dump(), user_id=current_user.id)
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry
@router.get("/{log_id}", response_model=NutritionResponse)
async def get_nutrition(log_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> NutritionLog:
    result = await db.execute(select(NutritionLog).where(NutritionLog.id == log_id, NutritionLog.user_id == current_user.id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Nutrition log not found")
    return entry
@router.patch("/{log_id}", response_model=NutritionResponse)
async def update_nutrition(log_id: UUID, body: NutritionUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> NutritionLog:
    result = await db.execute(select(NutritionLog).where(NutritionLog.id == log_id, NutritionLog.user_id == current_user.id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Nutrition log not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    await db.commit()
    await db.refresh(entry)
    return entry
@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_nutrition(log_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> None:
    result = await db.execute(select(NutritionLog).where(NutritionLog.id == log_id, NutritionLog.user_id == current_user.id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Nutrition log not found")
    await db.delete(entry)
    await db.commit()