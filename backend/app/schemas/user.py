from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    curl_pattern: Optional[str] = None
    porosity: Optional[str] = None
    density: Optional[str] = None
    thickness: Optional[str] = None
    scalp_type: Optional[str] = None
    location: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    curl_pattern: Optional[str] = None
    porosity: Optional[str] = None
    density: Optional[str] = None
    thickness: Optional[str] = None
    scalp_type: Optional[str] = None
    location: Optional[str] = None


class UserProfile(BaseModel):
    curl_pattern: Optional[str] = None
    porosity: Optional[str] = None
    density: Optional[str] = None
    thickness: Optional[str] = None
    scalp_type: Optional[str] = None
    location: Optional[str] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
