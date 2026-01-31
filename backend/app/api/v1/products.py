from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.product import Product
from app.schemas.product import Product as ProductSchema, ProductCreate, ProductUpdate

router = APIRouter()


@router.post("", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new product"""
    db_product = Product(**product_data.model_dump(), user_id=current_user.id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("", response_model=List[ProductSchema])
async def get_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all products for current user (including unassigned / community products with user_id NULL)"""
    from sqlalchemy import or_
    products = db.query(Product).filter(
        or_(Product.user_id == current_user.id, Product.user_id.is_(None))
    ).all()
    return products


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
