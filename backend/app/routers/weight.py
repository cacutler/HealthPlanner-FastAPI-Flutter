from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence
from uuid import UUID
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.weight import WeightLog
from app.schemas.nutrition_weight import WeightCreate, WeightResponse
router = APIRouter(prefix="/weight", tags=["weight"])
@router.get("", response_model=list[WeightResponse])
async def list_weight_logs(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> Sequence[WeightLog]:
    result = await db.execute(select(WeightLog).where(WeightLog.user_id == current_user.id).order_by(WeightLog.logged_at.desc()))
    return result.scalars().all()
@router.post("", response_model=WeightResponse, status_code=status.HTTP_201_CREATED)
async def log_weight(body: WeightCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> WeightLog:
    entry = WeightLog(**body.model_dump(), user_id=current_user.id)
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry
@router.get("/{log_id}", response_model=WeightResponse)
async def get_weight_log(log_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> WeightLog:
    result = await db.execute(select(WeightLog).where(WeightLog.id == log_id, WeightLog.user_id == current_user.id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Weight log not found")
    return entry
@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_weight_log(log_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> None:
    result = await db.execute(select(WeightLog).where(WeightLog.id == log_id, WeightLog.user_id == current_user.id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Weight log not found")
    await db.delete(entry)
    await db.commit()