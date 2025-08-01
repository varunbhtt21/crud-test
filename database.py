

# database.py - Database configuration and connection setup
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL configuration from environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
DATABASE_URL = (
    os.getenv("DATABASE_URL_PROD") if ENVIRONMENT == "prod" 
    else os.getenv("DATABASE_URL_DEV", "sqlite+aiosqlite:///./test.db")
)
DB_ECHO = os.getenv("DB_ECHO", "true").lower() == "true"



# Create async engine
"""
create_async_engine() creates the database connection engine
- echo: Shows SQL queries in console (controlled by DB_ECHO env var)
- future=True: Uses SQLAlchemy 2.0 style
"""
engine = create_async_engine(
    DATABASE_URL,
    echo=DB_ECHO,
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
