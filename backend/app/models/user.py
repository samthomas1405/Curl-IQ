from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Hair profile (stored as JSONB)
    curl_pattern = Column(String)  # 2A, 2B, 2C, 3A, 3B, 3C, 4A, 4B, 4C
    porosity = Column(String)  # low, medium, high
    density = Column(String, nullable=True)  # low, medium, high
    thickness = Column(String, nullable=True)  # fine, medium, coarse
    scalp_type = Column(String, nullable=True)  # dry, oily, sensitive, normal
    location = Column(String, nullable=True)  # city, state, country for weather
    
    # Relationships
    products = relationship("Product", back_populates="owner", cascade="all, delete-orphan")
    routines = relationship("Routine", back_populates="owner", cascade="all, delete-orphan")
    routine_logs = relationship("RoutineLog", back_populates="user", cascade="all, delete-orphan")
