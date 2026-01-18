from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.outcome import Outcome
from app.models.routine_log import RoutineLog
from app.schemas.outcome import Outcome as OutcomeSchema, OutcomeCreate, OutcomeUpdate

router = APIRouter()


def calculate_overall_score(frizz: int, definition: int, softness: int, hold_hours: float = None) -> float:
    """Calculate overall score from ratings (inverted frizz, weighted)"""
    # Invert frizz (1 = no frizz = good, 5 = very frizzy = bad)
    # Higher definition and softness are better
    # Hold hours contribute if provided
    frizz_score = (6 - frizz) / 5.0  # Invert: 5->1, 1->5, normalize to 0-1
    definition_score = definition / 5.0
    softness_score = softness / 5.0
    
    # Weighted average (frizz 40%, definition 30%, softness 30%)
    base_score = (frizz_score * 0.4 + definition_score * 0.3 + softness_score * 0.3) * 5
    
    # If hold_hours provided, add bonus (max 24 hours = full point)
    if hold_hours:
        hold_bonus = min(hold_hours / 24.0, 1.0)  # Max 1 point
        return min(base_score + hold_bonus, 5.0)  # Cap at 5
    
    return base_score


@router.post("", response_model=OutcomeSchema, status_code=status.HTTP_201_CREATED)
async def create_outcome(
    outcome_data: OutcomeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create an outcome for a routine log"""
    # Verify the routine log belongs to the user
    log = db.query(RoutineLog).filter(
        RoutineLog.id == outcome_data.routine_log_id,
        RoutineLog.user_id == current_user.id
    ).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine log not found"
        )
    
    # Check if outcome already exists
    existing = db.query(Outcome).filter(Outcome.routine_log_id == outcome_data.routine_log_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Outcome already exists for this routine log"
        )
    
    # Calculate overall score
    overall_score = calculate_overall_score(
        outcome_data.frizz,
        outcome_data.definition,
        outcome_data.softness,
        outcome_data.hold_hours
    )
    
    db_outcome = Outcome(
        routine_log_id=outcome_data.routine_log_id,
        frizz=outcome_data.frizz,
        definition=outcome_data.definition,
        softness=outcome_data.softness,
        hold_hours=outcome_data.hold_hours,
        notes=outcome_data.notes,
        overall_score=overall_score
    )
    db.add(db_outcome)
    db.commit()
    db.refresh(db_outcome)
    return db_outcome


@router.get("", response_model=List[OutcomeSchema])
async def get_outcomes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all outcomes for current user"""
    outcomes = db.query(Outcome).join(RoutineLog).filter(
        RoutineLog.user_id == current_user.id
    ).all()
    return outcomes


@router.get("/{outcome_id}", response_model=OutcomeSchema)
async def get_outcome(
    outcome_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific outcome"""
    outcome = db.query(Outcome).join(RoutineLog).filter(
        Outcome.id == outcome_id,
        RoutineLog.user_id == current_user.id
    ).first()
    if not outcome:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Outcome not found"
        )
    return outcome


@router.put("/{outcome_id}", response_model=OutcomeSchema)
async def update_outcome(
    outcome_id: int,
    outcome_update: OutcomeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an outcome"""
    outcome = db.query(Outcome).join(RoutineLog).filter(
        Outcome.id == outcome_id,
        RoutineLog.user_id == current_user.id
    ).first()
    if not outcome:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Outcome not found"
        )
    
    update_data = outcome_update.model_dump(exclude_unset=True)
    
    # Recalculate overall score if ratings changed
    if any(key in update_data for key in ['frizz', 'definition', 'softness', 'hold_hours']):
        frizz = update_data.get('frizz', outcome.frizz)
        definition = update_data.get('definition', outcome.definition)
        softness = update_data.get('softness', outcome.softness)
        hold_hours = update_data.get('hold_hours', outcome.hold_hours)
        update_data['overall_score'] = calculate_overall_score(frizz, definition, softness, hold_hours)
    
    for field, value in update_data.items():
        setattr(outcome, field, value)
    
    db.commit()
    db.refresh(outcome)
    return outcome


@router.delete("/{outcome_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_outcome(
    outcome_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an outcome"""
    outcome = db.query(Outcome).join(RoutineLog).filter(
        Outcome.id == outcome_id,
        RoutineLog.user_id == current_user.id
    ).first()
    if not outcome:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Outcome not found"
        )
    
    db.delete(outcome)
    db.commit()
    return None
