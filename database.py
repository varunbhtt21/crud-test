

# database.py - Database configuration and connection setup
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
import os

# Database URL configuration
# For development (SQLite)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# For production (PostgreSQL)
# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# Create async engine
"""
create_async_engine() creates the database connection engine
- echo=True: Shows SQL queries in console (useful for debugging)
- future=True: Uses SQLAlchemy 2.0 style
"""
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    future=True
)

# Create session maker
"""
async_sessionmaker creates a factory for database sessions
- expire_on_commit=False: Keeps objects accessible after commit
"""
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for database models
Base = declarative_base()

# Database dependency for FastAPI
async def get_db():
    """
    Dependency that provides database session to FastAPI endpoints
    This ensures proper session lifecycle management
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session  # Provide session to endpoint
        except Exception as e:
            await session.rollback()  # Rollback on error
            raise e
        finally:
            await session.close()  # Always close session

# Function to create database tables
async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        # Drop all tables (for development only!)
        await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
