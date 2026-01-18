from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, DateTime, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class RoutineLog(Base):
    __tablename__ = "routine_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    routine_id = Column(Integer, ForeignKey("routines.id"), nullable=True)  # Can log without template
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=True)
    
    # Products used per step (JSONB): {"cleanse": [product_id1, product_id2], "condition": [product_id3], ...}
    products_used = Column(JSON, nullable=True)
    
    # Routine details
    wash_day = Column(Boolean, default=True)
    styling_method = Column(String, nullable=True)  # wash-and-go, twist-out, etc.
    drying_method = Column(String, nullable=True)  # air-dry, diffuser, etc.
    
    # Optional fields
    time_spent = Column(Integer, nullable=True)  # minutes
    notes = Column(String, nullable=True)
    photo_urls = Column(JSON, nullable=True)  # Array of S3 URLs
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="routine_logs")
    routine = relationship("Routine", back_populates="routine_logs")
    outcome = relationship("Outcome", back_populates="routine_log", uselist=False, cascade="all, delete-orphan")
