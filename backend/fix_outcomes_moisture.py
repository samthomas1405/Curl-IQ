#!/usr/bin/env python3
"""Script to remove moisture column from outcomes table"""

from sqlalchemy import create_engine, text
from app.core.config import settings

def remove_moisture_column():
    """Remove moisture column if it exists"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Check if column exists
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='outcomes' AND column_name='moisture'
        """)
        result = conn.execute(check_query)
        exists = result.fetchone() is not None
        
        if exists:
            print("Removing 'moisture' column from outcomes table...")
            # Remove the column
            alter_query = text("""
                ALTER TABLE outcomes 
                DROP COLUMN moisture
            """)
            conn.execute(alter_query)
            conn.commit()
            print("Successfully removed 'moisture' column")
        else:
            print("'moisture' column does not exist")
    
    engine.dispose()

if __name__ == "__main__":
    remove_moisture_column()
