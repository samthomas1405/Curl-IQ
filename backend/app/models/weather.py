from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String, nullable=False)  # city, state, country
    
    # Weather metrics
    humidity = Column(Float, nullable=False)  # percentage
    dew_point = Column(Float, nullable=False)  # celsius
    temperature = Column(Float, nullable=False)  # celsius
    wind_speed = Column(Float, nullable=True)  # m/s
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Index for efficient queries
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'date'),
    )
