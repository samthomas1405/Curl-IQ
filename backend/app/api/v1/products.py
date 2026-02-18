from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.product import Product
from app.schemas.product import Product as ProductSchema, ProductCreate, ProductUpdate
from app.services.product_deduplication import check_and_suggest_duplicate

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    force_create: bool = Query(False, description="Force creation even if duplicate found")
):
    """
    Create a new product with duplicate detection
    
    If a similar product exists (>=95% similarity), returns the existing product.
    If similarity is 85-95%, raises 409 Conflict with suggestion.
    Use ?force_create=true to create anyway.
    """
    # Check for duplicates
    duplicate_check = check_and_suggest_duplicate(
        db,
        product_data.brand,
        product_data.name,
        product_data.type,
        user_id=current_user.id
    )
    
    if duplicate_check["exists"]:
        if duplicate_check["similarity"] >= 0.95:
            # Very similar - return existing product with notification
            existing_product = duplicate_check["product"]
            # Link it to current user if it's a community product
            if existing_product.user_id is None:
                existing_product.user_id = current_user.id
                db.commit()
                db.refresh(existing_product)
            
            # Return product with duplicate notification in response
            from fastapi.responses import JSONResponse
            import json
            from datetime import datetime
            
            # Convert to dict with JSON-compatible datetime serialization
            product_dict = ProductSchema.model_validate(existing_product).model_dump(mode='json')
            product_dict["_duplicate_notification"] = f"Product already exists: {existing_product.brand} - {existing_product.name}"
            return JSONResponse(
                status_code=200,
                content=product_dict
            )
        elif duplicate_check["similarity"] >= 0.85 and not force_create:
            # Somewhat similar - raise conflict with suggestion
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": duplicate_check["message"],
                    "similar_product": {
                        "id": duplicate_check["product"].id,
                        "brand": duplicate_check["product"].brand,
                        "name": duplicate_check["product"].name,
                        "type": duplicate_check["product"].type
                    },
                    "similarity": duplicate_check["similarity"]
                }
            )
    
    # No duplicate found or force_create=True - create new product
    db_product = Product(**product_data.model_dump(), user_id=current_user.id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return ProductSchema.model_validate(db_product)


@router.get("", response_model=List[ProductSchema])
async def get_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    search: Optional[str] = None
):
    """
    Get all products for current user (including unassigned / community products with user_id NULL)
    Optionally search by brand or name
    """
    from sqlalchemy import or_
    query = db.query(Product).filter(
        or_(Product.user_id == current_user.id, Product.user_id.is_(None))
    )
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Product.brand.ilike(search_term),
                Product.name.ilike(search_term)
            )
        )
    
    products = query.all()
    return products


@router.get("/check-duplicate")
async def check_duplicate(
    brand: str,
    name: str,
    product_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if a similar product already exists before creating
    Useful for frontend to show suggestions to user
    """
    duplicate_check = check_and_suggest_duplicate(
        db, brand, name, product_type, user_id=current_user.id
    )
    
    return {
        "exists": duplicate_check["exists"],
        "similar_product": {
            "id": duplicate_check["product"].id,
            "brand": duplicate_check["product"].brand,
            "name": duplicate_check["product"].name,
            "type": duplicate_check["product"].type,
            "success_rate": duplicate_check["product"].success_rate,
            "usage_count": duplicate_check["product"].usage_count
        } if duplicate_check["product"] else None,
        "similarity": duplicate_check["similarity"],
        "message": duplicate_check["message"],
        "action": duplicate_check["action"]
    }


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific product"""
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.user_id == current_user.id
    ).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a product"""
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.user_id == current_user.id
    ).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a product"""
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.user_id == current_user.id
    ).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    return None
