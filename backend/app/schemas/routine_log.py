from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime, date, time


class RoutineLogBase(BaseModel):
    date: date
    time: Optional[time] = None
    products_used: Optional[Dict[str, List[int]]] = None
    wash_day: bool = True
    styling_method: Optional[str] = None
    drying_method: Optional[str] = None
    time_spent: Optional[int] = None
    notes: Optional[str] = None
    photo_urls: Optional[List[str]] = None


class RoutineLogCreate(RoutineLogBase):
    routine_id: Optional[int] = None


class RoutineLogUpdate(BaseModel):
    date: Optional[date] = None
    time: Optional[time] = None
    products_used: Optional[Dict[str, List[int]]] = None
    wash_day: Optional[bool] = None
    styling_method: Optional[str] = None
    drying_method: Optional[str] = None
    time_spent: Optional[int] = None
    notes: Optional[str] = None
    photo_urls: Optional[List[str]] = None


class RoutineLog(RoutineLogBase):
    id: int
    user_id: int
    routine_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
