#!/usr/bin/env python3
"""Script to add missing softness column to outcomes table"""

from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_outcomes_table():
    """Add softness column if it doesn't exist"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Check if column exists
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='outcomes' AND column_name='softness'
        """)
        result = conn.execute(check_query)
        exists = result.fetchone() is not None
        
        if not exists:
            print("Adding missing 'softness' column to outcomes table...")
            # Add the column with a default value for existing rows
            alter_query = text("""
                ALTER TABLE outcomes 
                ADD COLUMN softness INTEGER NOT NULL DEFAULT 3
            """)
            conn.execute(alter_query)
            conn.commit()
            print("Successfully added 'softness' column")
        else:
            print("'softness' column already exists")
    
    engine.dispose()

if __name__ == "__main__":
    fix_outcomes_table()
