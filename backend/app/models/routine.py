from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Routine(Base):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    is_template = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)
    
    # Steps stored as JSONB array: [{"step_type": "cleanse", "product_id": 1, "order": 1, "notes": ""}, ...]
    steps = Column(JSON, nullable=False)
    
    # Method tags: wash-and-go, twist-out, braid-out, silk-press-prep
    method_tags = Column(JSON, nullable=True)  # Array of strings
    
    # Drying method
    drying_method = Column(String, nullable=True)  # air-dry, diffuser, hooded-dryer
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="routines")
    routine_logs = relationship("RoutineLog", back_populates="routine", cascade="all, delete-orphan")
