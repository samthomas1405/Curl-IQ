from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class RoutineBase(BaseModel):
    name: str
    is_template: bool = True
    is_public: bool = False
    steps: List[Dict[str, Any]]  # [{"step_type": "cleanse", "product_id": 1, "order": 1, "notes": ""}]
    method_tags: Optional[List[str]] = None
    drying_method: Optional[str] = None


class RoutineCreate(RoutineBase):
    pass


class RoutineUpdate(BaseModel):
    name: Optional[str] = None
    is_template: Optional[bool] = None
    is_public: Optional[bool] = None
    steps: Optional[List[Dict[str, Any]]] = None
    method_tags: Optional[List[str]] = None
    drying_method: Optional[str] = None


class Routine(RoutineBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
