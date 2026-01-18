#!/usr/bin/env python3
"""Script to delete a user from the database"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.user import User

# Create database connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def delete_user(email: str):
    """Delete a user by email"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            db.delete(user)
            db.commit()
            print(f"✅ User '{email}' deleted successfully")
        else:
            print(f"❌ User '{email}' not found")
    except Exception as e:
        db.rollback()
        print(f"❌ Error deleting user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python delete_user.py <email>")
        print("Example: python delete_user.py user@example.com")
        sys.exit(1)
    
    email = sys.argv[1]
    delete_user(email)
