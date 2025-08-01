# main.py - Basic FastAPI application setup
from fastapi import FastAPI
from database import create_tables
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
    try:
        await create_tables()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("⚠️  App will start but database features won't work")
        print("⚠️  Check your AWS RDS security group and network configuration")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

# Test database connection endpoint
@app.get("/test-db")
async def test_database_connection():
    """
    Test endpoint to verify database connection
    This version doesn't use dependency injection to avoid startup errors
    """
    try:
        from database import AsyncSessionLocal
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return {"status": "success", "message": "Database connection successful"}
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Database connection failed: {str(e)}",
            "suggestion": "Check AWS RDS security group and network configuration"
        }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True  # Auto-reload on code changes
    )
