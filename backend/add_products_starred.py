#!/usr/bin/env python3
"""Script to add is_starred column to products table if missing."""

from sqlalchemy import create_engine, text
from app.core.config import settings

def add_starred_column():
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'products' AND column_name = 'is_starred'
        """))
        if result.fetchone() is None:
            print("Adding 'is_starred' column to products table...")
            conn.execute(text("""
                ALTER TABLE products ADD COLUMN is_starred BOOLEAN NOT NULL DEFAULT FALSE
            """))
            conn.commit()
            print("Done.")
        else:
            print("'is_starred' already exists.")
    engine.dispose()

if __name__ == "__main__":
    add_starred_column()
