from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
class NutritionCreate(BaseModel):# ── Nutrition schemas ─────────────────────────────────────────────────────────
    calories: int
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    logged_at: datetime
class NutritionUpdate(BaseModel):
    calories: Optional[int] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    logged_at: Optional[datetime] = None
class NutritionResponse(BaseModel):
    id: UUID
    user_id: UUID
    calories: int
    protein_g: Optional[float]
    carbs_g: Optional[float]
    fat_g: Optional[float]
    logged_at: datetime
    model_config = {"from_attributes": True}
class WeightCreate(BaseModel):# ── Weight schemas ────────────────────────────────────────────────────────────
    weight_lbs: float
    logged_at: datetime
class WeightResponse(BaseModel):
    id: UUID
    user_id: UUID
    weight_lbs: float
    logged_at: datetime
    model_config = {"from_attributes": True}