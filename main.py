# main.py - Basic FastAPI application setup
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, create_tables
import uvicorn

# Create FastAPI application
app = FastAPI(
    title="User Management API",
    description="A comprehensive user and post management system",
    version="1.0.0"
)

# Startup event to create database tables
@app.on_event("startup")
async def startup_event():
    """
    This runs when the FastAPI application starts
    Creates all database tables if they don't exist
    """
    print("Creating database tables...")
    await create_tables()
    print("Database tables created successfully!")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

# Test database connection endpoint
@app.get("/test-db")
async def test_database_connection(db: AsyncSession = Depends(get_db)):
    """
    Test endpoint to verify database connection
    Demonstrates basic dependency injection
    """
    try:
        # Simple query to test connection
        result = await db.execute("SELECT 1")
        return {"status": "success", "message": "Database connection successful"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True  # Auto-reload on code changes
    )
