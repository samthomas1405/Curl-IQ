"""
Recommendation Service
Content-based filtering for product and routine recommendations
Uses feature similarity and user history
"""
from typing import Dict, List, Optional
import numpy as np
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.routine import Routine
from app.models.routine_log import RoutineLog
from app.models.outcome import Outcome
from app.models.user import User


class RecommendationService:
    """Service for generating personalized recommendations"""
    
    def __init__(self):
        pass
    
    def _encode_hair_profile(self, user: User) -> Dict[str, float]:
        """Encode hair profile as feature vector"""
        # Curl pattern encoding (2A-4C)
        curl_pattern = user.curl_pattern or "3B"
        curl_number = float(curl_pattern[0]) if curl_pattern[0].isdigit() else 3.0
        curl_letter = {"A": 1.0, "B": 2.0, "C": 3.0}.get(curl_pattern[1] if len(curl_pattern) > 1 else "B", 2.0)
        
        # Porosity encoding
        porosity_map = {"low": 1.0, "medium": 2.0, "high": 3.0}
        porosity = porosity_map.get(user.porosity, 2.0)
        
        # Density encoding
        density_map = {"low": 1.0, "medium": 2.0, "high": 3.0}
        density = density_map.get(user.density, 2.0)
        
        # Thickness encoding
        thickness_map = {"fine": 1.0, "medium": 2.0, "coarse": 3.0}
        thickness = thickness_map.get(user.thickness, 2.0)
        
        return {
            "curl_number": curl_number,
            "curl_letter": curl_letter,
            "porosity": porosity,
            "density": density,
            "thickness": thickness
        }
    
    def _calculate_similarity(self, profile1: Dict, profile2: Dict) -> float:
        """Calculate cosine similarity between two profiles"""
        keys = ["curl_number", "curl_letter", "porosity", "density", "thickness"]
        vec1 = np.array([profile1.get(k, 0) for k in keys])
        vec2 = np.array([profile2.get(k, 0) for k in keys])
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def recommend_products(
        self, 
        user: User, 
        db: Session, 
        limit: int = 5,
        exclude_owned: bool = True
    ) -> List[Dict]:
        """
        Recommend products based on:
        1. Hair profile similarity to other users
        2. Success rate of products
        3. User's historical preferences
        """
        user_profile = self._encode_hair_profile(user)
        
        # Get all products (relaxed criteria to include products with low/no usage)
        products = db.query(Product).filter(
            Product.usage_count >= 0  # Include all products, even with no usage yet
        ).all()
        
        if exclude_owned:
            products = [p for p in products if p.user_id != user.id]
        
        # If no products after filtering, include user's own products
        if not products:
            products = db.query(Product).filter(
                Product.user_id == user.id
            ).all()
        
        # Score products
        scored_products = []
        for product in products:
            score = 0.0
            
            # Base score: success rate (if available)
            if product.success_rate > 0:
                score += product.success_rate * 0.4
            else:
                # Give base score for products without usage data
                score += 0.2
            
            # Usage count bonus (more data = more reliable)
            if product.usage_count > 0:
                usage_bonus = min(product.usage_count / 10.0, 1.0) * 0.2
                score += usage_bonus
            else:
                # Give small bonus for new products
                score += 0.1
            
            # Find users who used this product successfully
            # (In a real system, we'd query this from the database)
            # For now, we'll use success_rate as a proxy
            
            # Type preference (if user has used similar products successfully)
            user_products = db.query(Product).filter(
                Product.user_id == user.id,
                Product.type == product.type
            ).all()
            if user_products:
                avg_success = np.mean([p.success_rate for p in user_products if p.success_rate > 0])
                if avg_success > 0:
                    score += avg_success * 0.4
            
            scored_products.append({
                "product": product,
                "score": score,
                "reason": f"Success rate: {product.success_rate:.1f}%, Used {product.usage_count} times"
            })
        
        # Sort by score
        scored_products.sort(key=lambda x: x["score"], reverse=True)
        
        return [
            {
                "id": item["product"].id,
                "brand": item["product"].brand,
                "name": item["product"].name,
                "type": item["product"].type,
                "success_rate": item["product"].success_rate,
                "usage_count": item["product"].usage_count,
                "score": item["score"],
                "reason": item["reason"]
            }
            for item in scored_products[:limit]
        ]
    
    def recommend_routines(
        self,
        user: User,
        db: Session,
        limit: int = 3
    ) -> List[Dict]:
        """
        Recommend routines based on:
        1. Similar users' successful routines
        2. User's hair profile
        3. Routine success rates
        """
        user_profile = self._encode_hair_profile(user)
        
        # Get routines with outcomes
        routines = db.query(Routine).join(
            RoutineLog, Routine.id == RoutineLog.routine_id
        ).join(
            Outcome, RoutineLog.id == Outcome.routine_log_id
        ).filter(
            Routine.user_id != user.id,  # Not user's own routines
            Routine.is_public == True  # Only public routines
        ).all()
        
        if not routines:
            # Fallback: recommend user's own best routines
            routines = db.query(Routine).filter(
                Routine.user_id == user.id
            ).all()
        
        # Score routines
        scored_routines = []
        for routine in routines:
            # Get average outcome for this routine
            avg_outcome = db.query(
                Outcome.overall_score
            ).join(
                RoutineLog, Outcome.routine_log_id == RoutineLog.id
            ).filter(
                RoutineLog.routine_id == routine.id
            ).all()
            
            if avg_outcome:
                avg_score = np.mean([o.overall_score for o in avg_outcome])
                log_count = len(avg_outcome)
                
                # Score based on average outcome and sample size
                score = avg_score * 0.6 + min(log_count / 5.0, 1.0) * 0.4
                
                scored_routines.append({
                    "routine": routine,
                    "score": score,
                    "avg_score": avg_score,
                    "log_count": log_count
                })
        
        # Sort by score
        scored_routines.sort(key=lambda x: x["score"], reverse=True)
        
        return [
            {
                "id": item["routine"].id,
                "name": item["routine"].name,
                "steps": item["routine"].steps,
                "method_tags": item["routine"].method_tags,
                "drying_method": item["routine"].drying_method,
                "score": item["score"],
                "avg_score": item["avg_score"],
                "log_count": item["log_count"],
                "reason": f"Average score: {item['avg_score']:.1f} from {item['log_count']} logs"
            }
            for item in scored_routines[:limit]
        ]
    
    def get_personalized_insights(
        self,
        user: User,
        db: Session
    ) -> List[Dict]:
        """
        Generate personalized insights based on user's data
        """
        insights = []
        
        # Get user's outcomes
        outcomes = db.query(Outcome).join(
            RoutineLog, Outcome.routine_log_id == RoutineLog.id
        ).filter(
            RoutineLog.user_id == user.id
        ).all()
        
        if len(outcomes) < 5:
            return [{
                "type": "info",
                "message": "Log more routines to get personalized insights!",
                "confidence": "low"
            }]
        
        # Best performing product type
        product_performance = {}
        for outcome in outcomes:
            log = outcome.routine_log
            if log.products_used:
                for step, product_id in log.products_used.items():
                    product = db.query(Product).filter(Product.id == product_id).first()
                    if product:
                        product_type = product.type
                        if product_type not in product_performance:
                            product_performance[product_type] = []
                        product_performance[product_type].append(outcome.overall_score)
        
        if product_performance:
            avg_by_type = {
                ptype: np.mean(scores) 
                for ptype, scores in product_performance.items()
            }
            best_type = max(avg_by_type.items(), key=lambda x: x[1])
            insights.append({
                "type": "product_performance",
                "message": f"{best_type[0].title()} products work best for you (avg score: {best_type[1]:.1f})",
                "confidence": "medium",
                "sample_size": len(product_performance[best_type[0]])
            })
        
        # Best drying method
        drying_performance = {}
        for outcome in outcomes:
            log = outcome.routine_log
            if log.drying_method:
                if log.drying_method not in drying_performance:
                    drying_performance[log.drying_method] = []
                drying_performance[log.drying_method].append(outcome.overall_score)
        
        if len(drying_performance) > 1:
            avg_by_drying = {
                method: np.mean(scores)
                for method, scores in drying_performance.items()
            }
            best_drying = max(avg_by_drying.items(), key=lambda x: x[1])
            insights.append({
                "type": "drying_method",
                "message": f"{best_drying[0].replace('-', ' ').title()} gives you the best results",
                "confidence": "medium",
                "sample_size": len(drying_performance[best_drying[0]])
            })
        
        return insights


# Singleton instance
recommendation_service = RecommendationService()
