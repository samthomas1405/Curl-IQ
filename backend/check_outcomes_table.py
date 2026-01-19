#!/usr/bin/env python3
"""Script to check outcomes table structure"""

from sqlalchemy import create_engine, text
from app.core.config import settings

def check_outcomes_table():
    """Check outcomes table columns"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        query = text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name='outcomes'
            ORDER BY ordinal_position
        """)
        result = conn.execute(query)
        columns = result.fetchall()
        
        print("Outcomes table columns:")
        print("-" * 50)
        for col in columns:
            print(f"{col[0]:20} {col[1]:15} nullable={col[2]}")
        
        # Check specifically for softness
        softness_exists = any(col[0] == 'softness' for col in columns)
        print("-" * 50)
        if softness_exists:
            print("softness column EXISTS")
        else:
            print("softness column MISSING")
    
    engine.dispose()

if __name__ == "__main__":
    check_outcomes_table()
