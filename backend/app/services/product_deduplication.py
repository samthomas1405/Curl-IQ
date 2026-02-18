"""
Product Deduplication Service
Prevents duplicate products by checking for similar existing products
"""
import re
from sqlalchemy.orm import Session
from typing import Optional, Tuple
from difflib import SequenceMatcher
from app.models.product import Product


def normalize_text(text: str) -> str:
    """Normalize text for comparison - handles hyphens, spaces, and punctuation"""
    # Convert to lowercase and strip
    normalized = text.lower().strip()
    # Replace hyphens with spaces (so "Leave-In" becomes "leave in")
    normalized = normalized.replace('-', ' ')
    # Remove extra whitespace
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized


def similarity_score(str1: str, str2: str) -> float:
    """Calculate similarity score between two strings (0-1)"""
    norm1 = normalize_text(str1)
    norm2 = normalize_text(str2)
    
    # Check if one is a substring of the other (common case: "Classic Leave-In" vs "Classic Leave-In Conditioner")
    if norm1 in norm2 or norm2 in norm1:
        # If one contains the other, give high similarity
        shorter = min(len(norm1), len(norm2))
        longer = max(len(norm1), len(norm2))
        # Base score on how much of the shorter string is in the longer one
        return min(0.95, shorter / longer + 0.3)  # At least 0.3 bonus, cap at 0.95
    
    # Use sequence matcher for other cases
    return SequenceMatcher(None, norm1, norm2).ratio()


def find_similar_product(
    db: Session,
    brand: str,
    name: str,
    product_type: str,
    threshold: float = 0.80  # Lowered threshold to catch more cases
) -> Tuple[Optional[Product], float]:
    """
    Find similar products in the database
    
    Args:
        db: Database session
        brand: Product brand
        name: Product name
        product_type: Product type
        threshold: Similarity threshold (0-1), default 0.85
    
    Returns:
        Tuple of (Product or None, similarity_score)
    """
    # First, check for exact match (case-insensitive)
    exact_match = db.query(Product).filter(
        Product.brand.ilike(brand.strip()),
        Product.name.ilike(name.strip()),
        Product.type == product_type
    ).first()
    
    if exact_match:
        return exact_match, 1.0
    
    # Then check for similar products (fuzzy matching)
    all_products = db.query(Product).filter(
        Product.type == product_type
    ).all()
    
    best_match = None
    best_score = 0.0
    
    normalized_brand = normalize_text(brand)
    normalized_name = normalize_text(name)
    
    for product in all_products:
        # Check if brands match exactly (case-insensitive)
        brand_match = normalize_text(brand) == normalize_text(product.brand)
        
        if not brand_match:
            continue  # Skip if brands don't match
        
        # Special case: if one name contains the other, treat as very similar
        # Check this FIRST before fuzzy matching (more reliable for substring cases)
        norm_name1 = normalize_text(name)
        norm_name2 = normalize_text(product.name)
        
        if norm_name1 in norm_name2 or norm_name2 in norm_name1:
            # One is substring of other - very likely duplicate
            # Check if the shorter name is substantial (at least 10 chars) to avoid false positives
            shorter = min(len(norm_name1), len(norm_name2))
            if shorter >= 10:  # Only if shorter name is substantial
                name_sim = 0.98  # Very high similarity - treat as duplicate
            elif shorter >= 5:  # Medium length - still likely duplicate
                name_sim = 0.90  # High similarity
            else:
                # Too short, use regular similarity
                name_sim = similarity_score(name, product.name)
        else:
            # Calculate name similarity using fuzzy matching
            name_sim = similarity_score(name, product.name)
        
        # Since brands match, we only need to check name similarity
        # But we'll use a combined score for consistency
        combined_score = (1.0 * 0.3) + (name_sim * 0.7)  # Brand is 1.0 since it matches
        
        if combined_score > best_score and combined_score >= threshold:
            best_score = combined_score
            best_match = product
    
    return best_match, best_score


def check_and_suggest_duplicate(
    db: Session,
    brand: str,
    name: str,
    product_type: str,
    user_id: Optional[int] = None
) -> dict:
    """
    Check for duplicate products and return suggestion
    
    Args:
        db: Database session
        brand: Product brand
        name: Product name
        product_type: Product type
        user_id: Current user ID (to exclude user's own products if needed)
    
    Returns:
        Dictionary with:
        - exists: bool - whether a similar product exists
        - product: Product or None - the similar product if found
        - similarity: float - similarity score
        - message: str - message to show user
    """
    similar_product, similarity = find_similar_product(
        db, brand, name, product_type, threshold=0.80  # Lowered to catch substring matches
    )
    
    if similar_product:
        if similarity >= 0.95:
            # Very similar - likely duplicate
            return {
                "exists": True,
                "product": similar_product,
                "similarity": similarity,
                "message": f"Similar product found: {similar_product.brand} - {similar_product.name}",
                "action": "suggest_existing"
            }
        elif similarity >= 0.85:
            # Somewhat similar - warn user
            return {
                "exists": True,
                "product": similar_product,
                "similarity": similarity,
                "message": f"Similar product exists: {similar_product.brand} - {similar_product.name} ({(similarity*100):.0f}% similar). Continue anyway?",
                "action": "warn"
            }
    
    return {
        "exists": False,
        "product": None,
        "similarity": 0.0,
        "message": None,
        "action": "create_new"
    }
