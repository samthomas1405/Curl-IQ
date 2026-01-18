from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OutcomeBase(BaseModel):
    frizz: int = Field(..., ge=1, le=5)
    definition: int = Field(..., ge=1, le=5)
    softness: int = Field(..., ge=1, le=5)
    hold_hours: Optional[float] = None
    notes: Optional[str] = None


class OutcomeCreate(OutcomeBase):
    routine_log_id: int


class OutcomeUpdate(BaseModel):
    frizz: Optional[int] = Field(None, ge=1, le=5)
    definition: Optional[int] = Field(None, ge=1, le=5)
    softness: Optional[int] = Field(None, ge=1, le=5)
    hold_hours: Optional[float] = None
    notes: Optional[str] = None


class Outcome(OutcomeBase):
    id: int
    routine_log_id: int
    overall_score: float
    rated_at: datetime

    class Config:
        from_attributes = True
