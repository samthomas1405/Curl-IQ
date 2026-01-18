from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import httpx
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.weather import WeatherData
from app.schemas.weather import WeatherData as WeatherDataSchema, WeatherDataCreate

router = APIRouter()


async def fetch_weather_from_api(location: str) -> dict:
    """Fetch weather data from OpenWeatherMap API"""
    if not settings.WEATHER_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Weather API key not configured"
        )
    
    # Simple location parsing (can be enhanced)
    # For now, assume location is "city,state,country" or just "city"
    city = location.split(",")[0].strip()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.WEATHER_API_URL}/weather",
                params={
                    "q": city,
                    "appid": settings.WEATHER_API_KEY,
                    "units": "metric"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "humidity": data["main"]["humidity"],
                "dew_point": data.get("dew_point", data["main"]["temp"] - (100 - data["main"]["humidity"]) / 5),  # Approximation
                "temperature": data["main"]["temp"],
                "wind_speed": data.get("wind", {}).get("speed", 0)
            }
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to fetch weather data: {str(e)}"
            )


@router.post("/fetch", response_model=WeatherDataSchema, status_code=status.HTTP_201_CREATED)
async def fetch_and_save_weather(
    target_date: date,
    location: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetch weather data for a specific date and location, then save it"""
    # Use user's location if not provided
    if not location:
        if not current_user.location:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Location not provided and user has no default location"
            )
        location = current_user.location
    
    # Check if weather data already exists for this date
    existing = db.query(WeatherData).filter(
        WeatherData.user_id == current_user.id,
        WeatherData.date == target_date,
        WeatherData.location == location
    ).first()
    
    if existing:
        return existing
    
    # Fetch from API
    weather_data = await fetch_weather_from_api(location)
    
    # Save to database
    db_weather = WeatherData(
        user_id=current_user.id,
        date=target_date,
        location=location,
        **weather_data
    )
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather


@router.get("", response_model=List[WeatherDataSchema])
async def get_weather_data(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weather data for current user"""
    query = db.query(WeatherData).filter(WeatherData.user_id == current_user.id)
    
    if start_date:
        query = query.filter(WeatherData.date >= start_date)
    if end_date:
        query = query.filter(WeatherData.date <= end_date)
    
    weather_data = query.order_by(WeatherData.date.desc()).all()
    return weather_data


@router.get("/{weather_id}", response_model=WeatherDataSchema)
async def get_weather(
    weather_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific weather data entry"""
    weather = db.query(WeatherData).filter(
        WeatherData.id == weather_id,
        WeatherData.user_id == current_user.id
    ).first()
    if not weather:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather data not found"
        )
    return weather
