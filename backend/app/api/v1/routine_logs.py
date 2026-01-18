from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.routine_log import RoutineLog
from app.schemas.routine_log import RoutineLog as RoutineLogSchema, RoutineLogCreate, RoutineLogUpdate

router = APIRouter()


@router.post("", response_model=RoutineLogSchema, status_code=status.HTTP_201_CREATED)
async def create_routine_log(
    log_data: RoutineLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new routine log"""
    db_log = RoutineLog(**log_data.model_dump(), user_id=current_user.id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@router.get("", response_model=List[RoutineLogSchema])
async def get_routine_logs(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get routine logs for current user"""
    query = db.query(RoutineLog).filter(RoutineLog.user_id == current_user.id)
    
    if start_date:
        query = query.filter(RoutineLog.date >= start_date)
    if end_date:
        query = query.filter(RoutineLog.date <= end_date)
    
    logs = query.order_by(RoutineLog.date.desc()).offset(skip).limit(limit).all()
    return logs


@router.get("/{log_id}", response_model=RoutineLogSchema)
async def get_routine_log(
    log_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific routine log"""
    log = db.query(RoutineLog).filter(
        RoutineLog.id == log_id,
        RoutineLog.user_id == current_user.id
    ).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine log not found"
        )
    return log


@router.put("/{log_id}", response_model=RoutineLogSchema)
async def update_routine_log(
    log_id: int,
    log_update: RoutineLogUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a routine log"""
    log = db.query(RoutineLog).filter(
        RoutineLog.id == log_id,
        RoutineLog.user_id == current_user.id
    ).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine log not found"
        )
    
    update_data = log_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(log, field, value)
    
    db.commit()
    db.refresh(log)
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_routine_log(
    log_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a routine log"""
    log = db.query(RoutineLog).filter(
        RoutineLog.id == log_id,
        RoutineLog.user_id == current_user.id
    ).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine log not found"
        )
    
    db.delete(log)
    db.commit()
    return None
