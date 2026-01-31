from sqlalchemy import Column, Integer, String, Float, ForeignKey, ARRAY, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for community products
    brand = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # shampoo, conditioner, leave-in, cream, gel, mousse, oil
    ingredients = Column(ARRAY(String), nullable=True)
    notes = Column(String, nullable=True)
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)  # Computed from outcomes
    is_starred = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="products")
