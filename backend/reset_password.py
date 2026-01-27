"""Script to reset a user's password in local development"""
import sys
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def reset_password(email: str, new_password: str):
    """Reset a user's password"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"User with email {email} not found in database.")
            print("\nAvailable users:")
            users = db.query(User).all()
            for u in users:
                print(f"  - {u.email} (ID: {u.id})")
            return
        
        user.password_hash = get_password_hash(new_password)
        db.commit()
        print(f"Password reset successfully for {email}")
        print(f"New password: {new_password}")
    except Exception as e:
        print(f"Error resetting password: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reset_password.py <email> <new_password>")
        print("\nExample: python reset_password.py ankithavin@gmail.com password123")
        sys.exit(1)
    
    email = sys.argv[1]
    new_password = sys.argv[2]
    reset_password(email, new_password)
