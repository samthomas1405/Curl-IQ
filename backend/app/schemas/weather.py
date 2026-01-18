from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class WeatherDataBase(BaseModel):
    date: date
    location: str
    humidity: float
    dew_point: float
    temperature: float
    wind_speed: Optional[float] = None


class WeatherDataCreate(WeatherDataBase):
    user_id: int


class WeatherData(WeatherDataBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
