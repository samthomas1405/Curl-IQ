"""
AI/ML API Endpoints
Provides endpoints for:
- Outcome prediction
- Smart recommendations
- AI-powered insights
- Pattern detection
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import date, timedelta
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.routine_log import RoutineLog
from app.models.outcome import Outcome
from app.models.product import Product
from app.models.routine import Routine
from app.models.weather import WeatherData
from app.services.ml_service import ml_service
from app.services.llm_service import llm_service
from app.services.recommendation_service import recommendation_service
from sqlalchemy import func, and_

router = APIRouter()


@router.post("/predict-outcome")
async def predict_outcome(
    routine_data: Dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Predict outcome score for a routine before performing it
    
    Request body should include:
    - routine_id (optional)
    - products (list of product IDs)
    - drying_method
    - weather data (optional, will fetch if not provided)
    """
    try:
        # Get user's hair profile
        user_profile = {
            "curl_pattern": current_user.curl_pattern or "3B",
            "porosity": current_user.porosity or "medium",
            "density": current_user.density or "medium",
            "thickness": current_user.thickness or "medium",
            "scalp_type": current_user.scalp_type or "normal"
        }
        
        # Get weather data
        weather = None
        if routine_data.get("date"):
            weather = db.query(WeatherData).filter(
                and_(
                    WeatherData.user_id == current_user.id,
                    WeatherData.date == routine_data["date"]
                )
            ).first()
        
        if not weather and current_user.location:
            # Try to fetch weather (you'd call your weather API here)
            weather = {
                "humidity": 50.0,
                "temperature": 70.0,
                "dew_point": 55.0
            }
        else:
            weather = {
                "humidity": weather.humidity if weather else 50.0,
                "temperature": weather.temperature if weather else 70.0,
                "dew_point": weather.dew_point if weather else 55.0
            }
        
        # Get historical average
        historical_avg = db.query(func.avg(Outcome.overall_score)).join(
            RoutineLog, Outcome.routine_log_id == RoutineLog.id
        ).filter(
            RoutineLog.user_id == current_user.id
        ).scalar() or 3.5
        
        # Prepare features
        features = {
            **user_profile,
            **weather,
            "drying_method": routine_data.get("drying_method", "air-dry"),
            "product_type": routine_data.get("product_type", "gel"),  # Most common type
            "num_products": len(routine_data.get("products", [])),
            "historical_avg_score": float(historical_avg)
        }
        
        # Predict
        prediction = ml_service.predict(features)
        
        return {
            "prediction": prediction,
            "user_profile": user_profile,
            "weather": weather
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.get("/recommendations/products")
async def get_product_recommendations(
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered product recommendations"""
    try:
        recommendations = recommendation_service.recommend_products(
            user=current_user,
            db=db,
            limit=limit
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")


@router.get("/recommendations/routines")
async def get_routine_recommendations(
    limit: int = 3,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered routine recommendations"""
    try:
        recommendations = recommendation_service.recommend_routines(
            user=current_user,
            db=db,
            limit=limit
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")


@router.get("/insights/ai")
async def get_ai_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered insights with LLM explanations
    Combines statistical insights with natural language explanations
    """
    try:
        # Get personalized insights
        insights = recommendation_service.get_personalized_insights(
            user=current_user,
            db=db
        )
        
        # Enhance with LLM explanations
        enhanced_insights = []
        for insight in insights:
            llm_explanation = llm_service.generate_insight_explanation(insight)
            enhanced_insights.append({
                **insight,
                "ai_explanation": llm_explanation,
                "has_ai": llm_explanation is not None
            })
        
        return {"insights": enhanced_insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insight generation error: {str(e)}")


@router.post("/train-model")
async def train_prediction_model(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Train the ML prediction model on user's historical data
    Requires at least 10 logged routines with outcomes
    """
    try:
        # Get all user's routine logs with outcomes
        logs = db.query(RoutineLog).join(
            Outcome, RoutineLog.id == Outcome.routine_log_id
        ).filter(
            RoutineLog.user_id == current_user.id
        ).all()
        
        if len(logs) < 10:
            raise HTTPException(
                status_code=400,
                detail="Need at least 10 logged routines with outcomes to train model"
            )
        
        # Prepare training data
        training_data = []
        for log in logs:
            outcome = log.outcome
            
            # Get weather data
            weather = db.query(WeatherData).filter(
                and_(
                    WeatherData.user_id == current_user.id,
                    WeatherData.date == log.date
                )
            ).first()
            
            # Get routine
            routine = db.query(Routine).filter(Routine.id == log.routine_id).first()
            
            # Prepare features
            features = {
                "curl_pattern": current_user.curl_pattern or "3B",
                "porosity": current_user.porosity or "medium",
                "density": current_user.density or "medium",
                "thickness": current_user.thickness or "medium",
                "scalp_type": current_user.scalp_type or "normal",
                "humidity": weather.humidity if weather else 50.0,
                "temperature": weather.temperature if weather else 70.0,
                "dew_point": weather.dew_point if weather else 55.0,
                "drying_method": log.drying_method or "air-dry",
                "product_type": "gel",  # Simplified
                "num_products": len(log.products_used) if log.products_used else 1,
                "historical_avg_score": 3.5  # Simplified
            }
            
            # Add target
            features["overall_score"] = outcome.overall_score
            
            training_data.append(features)
        
        # Train model
        metrics = ml_service.train_model(training_data)
        
        return {
            "message": "Model trained successfully",
            "metrics": metrics
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")


@router.get("/insights/patterns")
async def detect_patterns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Detect patterns in user's routine data using statistical analysis
    """
    try:
        # Get outcomes with full context
        outcomes = db.query(Outcome).join(
            RoutineLog, Outcome.routine_log_id == RoutineLog.id
        ).filter(
            RoutineLog.user_id == current_user.id
        ).all()
        
        if len(outcomes) < 5:
            return {
                "patterns": [],
                "message": "Need at least 5 logged routines to detect patterns"
            }
        
        patterns = []
        
        # Pattern 1: Time-based trends
        recent_outcomes = [o for o in outcomes if o.rated_at]
        if len(recent_outcomes) >= 5:
            recent_scores = [o.overall_score for o in recent_outcomes[-5:]]
            older_scores = [o.overall_score for o in recent_outcomes[:-5]] if len(recent_outcomes) > 5 else []
            
            if older_scores:
                recent_avg = sum(recent_scores) / len(recent_scores)
                older_avg = sum(older_scores) / len(older_scores)
                
                if recent_avg > older_avg + 0.5:
                    patterns.append({
                        "type": "improvement",
                        "message": f"Your recent routines are performing {((recent_avg - older_avg) / older_avg * 100):.1f}% better than earlier ones",
                        "confidence": "high",
                        "trend": "improving"
                    })
                elif recent_avg < older_avg - 0.5:
                    patterns.append({
                        "type": "decline",
                        "message": f"Your recent routines are performing {((older_avg - recent_avg) / older_avg * 100):.1f}% worse than earlier ones",
                        "confidence": "medium",
                        "trend": "declining"
                    })
        
        # Pattern 2: Product combinations
        product_combos = {}
        for outcome in outcomes:
            log = outcome.routine_log
            if log.products_used:
                combo_key = tuple(sorted(log.products_used.values()))
                if combo_key not in product_combos:
                    product_combos[combo_key] = []
                product_combos[combo_key].append(outcome.overall_score)
        
        if product_combos:
            avg_by_combo = {
                combo: sum(scores) / len(scores)
                for combo, scores in product_combos.items()
                if len(scores) >= 2
            }
            if avg_by_combo:
                best_combo = max(avg_by_combo.items(), key=lambda x: x[1])
                patterns.append({
                    "type": "product_combination",
                    "message": f"A specific product combination is working well (avg score: {best_combo[1]:.1f})",
                    "confidence": "medium",
                    "sample_size": len(product_combos[best_combo[0]])
                })
        
        return {"patterns": patterns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pattern detection error: {str(e)}")
