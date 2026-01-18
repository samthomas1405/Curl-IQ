from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Outcome(Base):
    __tablename__ = "outcomes"

    id = Column(Integer, primary_key=True, index=True)
    routine_log_id = Column(Integer, ForeignKey("routine_logs.id"), unique=True, nullable=False)
    
    # Ratings (1-5 scale)
    frizz = Column(Integer, nullable=False)  # 1 = no frizz, 5 = very frizzy
    definition = Column(Integer, nullable=False)  # 1 = no definition, 5 = very defined
    softness = Column(Integer, nullable=False)  # 1 = not soft, 5 = very soft
    
    # Hold/longevity (hours)
    hold_hours = Column(Float, nullable=True)
    
    # Computed overall score (weighted average)
    overall_score = Column(Float, nullable=False)
    
    # Optional notes
    notes = Column(String, nullable=True)
    
    # When was this rated
    rated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    routine_log = relationship("RoutineLog", back_populates="outcome")
