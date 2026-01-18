from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Dict, List, Any
from datetime import date, timedelta
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.routine_log import RoutineLog
from app.models.outcome import Outcome
from app.models.routine import Routine
from app.models.product import Product
from app.models.weather import WeatherData

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics and insights"""
    # Total logs
    total_logs = db.query(func.count(RoutineLog.id)).filter(
        RoutineLog.user_id == current_user.id
    ).scalar() or 0
    
    # Total outcomes
    total_outcomes = db.query(func.count(Outcome.id)).select_from(Outcome).join(
        RoutineLog, Outcome.routine_log_id == RoutineLog.id
    ).filter(
        RoutineLog.user_id == current_user.id
    ).scalar() or 0
    
    # Average scores
    avg_scores = db.query(
        func.avg(Outcome.frizz).label("avg_frizz"),
        func.avg(Outcome.definition).label("avg_definition"),
        func.avg(Outcome.softness).label("avg_softness"),
        func.avg(Outcome.overall_score).label("avg_overall"),
        func.avg(Outcome.hold_hours).label("avg_hold")
    ).select_from(Outcome).join(
        RoutineLog, Outcome.routine_log_id == RoutineLog.id
    ).filter(
        RoutineLog.user_id == current_user.id
    ).first()
    
    # Best routine (by average overall score)
    best_routine = db.query(
        Routine.id,
        Routine.name,
        func.avg(Outcome.overall_score).label("avg_score"),
        func.count(Outcome.id).label("log_count")
    ).select_from(Routine).join(
        RoutineLog, Routine.id == RoutineLog.routine_id
    ).join(
        Outcome, RoutineLog.id == Outcome.routine_log_id
    ).filter(
        Routine.user_id == current_user.id
    ).group_by(Routine.id, Routine.name).having(
        func.count(Outcome.id) >= 3  # At least 3 logs
    ).order_by(func.avg(Outcome.overall_score).desc()).first()
    
    # Best products (simplified - by success_rate)
    best_products = db.query(Product).filter(
        Product.user_id == current_user.id,
        Product.usage_count >= 3
    ).order_by(Product.success_rate.desc()).limit(5).all()
    
    return {
        "total_logs": total_logs,
        "total_outcomes": total_outcomes,
        "average_scores": {
            "frizz": round(avg_scores.avg_frizz, 2) if avg_scores and avg_scores.avg_frizz else None,
            "definition": round(avg_scores.avg_definition, 2) if avg_scores and avg_scores.avg_definition else None,
            "softness": round(avg_scores.avg_softness, 2) if avg_scores and avg_scores.avg_softness else None,
            "overall": round(avg_scores.avg_overall, 2) if avg_scores and avg_scores.avg_overall else None,
            "hold_hours": round(avg_scores.avg_hold, 2) if avg_scores and avg_scores.avg_hold else None,
        },
        "best_routine": {
            "id": best_routine.id,
            "name": best_routine.name,
            "average_score": round(best_routine.avg_score, 2),
            "log_count": best_routine.log_count
        } if best_routine else None,
        "best_products": [
            {
                "id": p.id,
                "brand": p.brand,
                "name": p.name,
                "type": p.type,
                "success_rate": round(p.success_rate, 2),
                "usage_count": p.usage_count
            }
            for p in best_products
        ]
    }


@router.get("/trends")
async def get_trends(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get trends over time"""
    start_date = date.today() - timedelta(days=days)
    
    # Get outcomes with dates
    trends = db.query(
        RoutineLog.date,
        func.avg(Outcome.frizz).label("avg_frizz"),
        func.avg(Outcome.definition).label("avg_definition"),
        func.avg(Outcome.softness).label("avg_softness"),
        func.avg(Outcome.overall_score).label("avg_overall")
    ).select_from(RoutineLog).join(
        Outcome, RoutineLog.id == Outcome.routine_log_id
    ).filter(
        and_(
            RoutineLog.user_id == current_user.id,
            RoutineLog.date >= start_date
        )
    ).group_by(RoutineLog.date).order_by(RoutineLog.date).all()
    
    return {
        "trends": [
            {
                "date": str(t.date),
                "frizz": round(t.avg_frizz, 2),
                "definition": round(t.avg_definition, 2),
                "softness": round(t.avg_softness, 2),
                "overall": round(t.avg_overall, 2)
            }
            for t in trends
        ]
    }


@router.get("/insights")
async def get_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get basic insights (simplified version)"""
    insights = []
    
    # Weather correlation (simplified)
    # Compare high humidity vs low humidity days
    high_humidity_threshold = 60.0
    low_humidity_threshold = 40.0
    
    high_humidity_outcomes = db.query(func.avg(Outcome.frizz)).select_from(Outcome).join(
        RoutineLog, Outcome.routine_log_id == RoutineLog.id
    ).join(
        WeatherData, and_(
            WeatherData.user_id == current_user.id,
            WeatherData.date == RoutineLog.date
        )
    ).filter(
        and_(
            RoutineLog.user_id == current_user.id,
            WeatherData.humidity >= high_humidity_threshold
        )
    ).scalar()
    
    low_humidity_outcomes = db.query(func.avg(Outcome.frizz)).select_from(Outcome).join(
        RoutineLog, Outcome.routine_log_id == RoutineLog.id
    ).join(
        WeatherData, and_(
            WeatherData.user_id == current_user.id,
            WeatherData.date == RoutineLog.date
        )
    ).filter(
        and_(
            RoutineLog.user_id == current_user.id,
            WeatherData.humidity <= low_humidity_threshold
        )
    ).scalar()
    
    if high_humidity_outcomes and low_humidity_outcomes:
        if high_humidity_outcomes > low_humidity_outcomes:
            insights.append({
                "type": "weather",
                "message": f"High humidity days (≥{high_humidity_threshold}%) show {round((high_humidity_outcomes - low_humidity_outcomes) / low_humidity_outcomes * 100, 1)}% higher frizz on average",
                "confidence": "medium"
            })
    
    return {"insights": insights}
