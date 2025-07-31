# schemas.py - Pydantic models for API validation and serialization
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime

# Base schemas
class UserBase(BaseModel):
    """Base user fields shared across different contexts"""
    username: str = Field(..., min_length=3, max_length=50, regex="^[a-zA-Z0-9_]+$")
    email: EmailStr  # Validates email format
    full_name: str = Field(..., min_length=1, max_length=100)

class PostBase(BaseModel):
    """Base post fields"""
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10)

# Create schemas (for API input)
class UserCreate(UserBase):
    """Schema for creating new users"""
    password: str = Field(..., min_length=8)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric (underscores allowed)')
        return v.lower()  # Convert to lowercase

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "password": "secretpassword123"
            }
        }

class PostCreate(PostBase):
    """Schema for creating new posts"""
    is_published: bool = False

# Update schemas (for API updates)
class UserUpdate(BaseModel):
    """Schema for updating users - all fields optional"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None

class PostUpdate(BaseModel):
    """Schema for updating posts"""
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    content: Optional[str] = Field(None, min_length=10)
    is_published: Optional[bool] = None

# Response schemas (for API output)
class UserResponse(UserBase):
    """Schema for user API responses"""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model

class PostResponse(PostBase):
    """Schema for post API responses"""
    id: int
    is_published: bool
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Nested response schemas (including relationships)
class PostWithAuthor(PostResponse):
    """Post response with author information"""
    author: UserResponse

class UserWithPosts(UserResponse):
    """User response with their posts"""
    posts: List[PostResponse] = []
