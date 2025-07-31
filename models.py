# models.py - Database models (SQLAlchemy)
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    """
    User database model - defines the 'users' table structure
    """
    __tablename__ = "users"  # Table name in database

    # Primary key - auto-incrementing integer
    id = Column(Integer, primary_key=True, index=True)

    # User fields with constraints
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Timestamps - automatically managed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to posts (one user can have many posts)
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    """
    Post database model - demonstrates relationships
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    is_published = Column(Boolean, default=False)

    # Foreign key relationship
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship back to user
    author = relationship("User", back_populates="posts")
