from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.user import SexType, ActivityLevel
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    height_in: Optional[int] = None
    weight_lbs: Optional[int] = None
    age: Optional[int] = None
    sex: Optional[SexType] = None
    activity_level: Optional[ActivityLevel] = None
class UserUpdate(BaseModel):
    height_in: Optional[int] = None
    weight_lbs: Optional[int] = None
    age: Optional[int] = None
    sex: Optional[SexType] = None
    activity_level: Optional[ActivityLevel] = None
class UserResponse(BaseModel):
    id: UUID
    email: str
    height_in: Optional[int]
    weight_lbs: Optional[int]
    age: Optional[int]
    sex: Optional[SexType]
    activity_level: Optional[ActivityLevel]
    created_at: datetime
    model_config = {"from_attributes": True}