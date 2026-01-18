from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.routine import Routine
from app.schemas.routine import Routine as RoutineSchema, RoutineCreate, RoutineUpdate

router = APIRouter()


@router.post("", response_model=RoutineSchema, status_code=status.HTTP_201_CREATED)
async def create_routine(
    routine_data: RoutineCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new routine template"""
    db_routine = Routine(**routine_data.model_dump(), user_id=current_user.id)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    return db_routine


@router.get("", response_model=List[RoutineSchema])
async def get_routines(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all routines for current user"""
    routines = db.query(Routine).filter(Routine.user_id == current_user.id).all()
    return routines


@router.get("/{routine_id}", response_model=RoutineSchema)
async def get_routine(
    routine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific routine"""
    routine = db.query(Routine).filter(
        Routine.id == routine_id,
        Routine.user_id == current_user.id
    ).first()
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
    return routine


@router.put("/{routine_id}", response_model=RoutineSchema)
async def update_routine(
    routine_id: int,
    routine_update: RoutineUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a routine"""
    routine = db.query(Routine).filter(
        Routine.id == routine_id,
        Routine.user_id == current_user.id
    ).first()
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
    
    update_data = routine_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(routine, field, value)
    
    db.commit()
    db.refresh(routine)
    return routine


@router.delete("/{routine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_routine(
    routine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a routine"""
    routine = db.query(Routine).filter(
        Routine.id == routine_id,
        Routine.user_id == current_user.id
    ).first()
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
    
    db.delete(routine)
    db.commit()
    return None
