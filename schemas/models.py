"""
Pydantic v2 models for the Task Management System.
All models use strict validation; failures return 422 errors automatically.
"""

from typing import Annotated, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# -----------------------------------------------------------------------------
# Profile Model (nested in UserCreate)
# -----------------------------------------------------------------------------
class Profile(BaseModel):
    """User profile with contact information."""

    full_name: str = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="Valid email address")
    phone: Optional[str] = Field(default=None, description="Optional phone number")


# -----------------------------------------------------------------------------
# User Models
# -----------------------------------------------------------------------------
class UserCreate(BaseModel):
    """Schema for creating a new user."""

    username: str = Field(..., description="Unique username")
    role: Literal["admin", "manager", "member"] = Field(
        ..., description="User role in the system"
    )
    profile: Profile = Field(..., description="User profile with contact details")


class User(UserCreate):
    """User response model (includes all creation fields, can be extended)."""

    id: int = Field(..., description="Unique user identifier")


# -----------------------------------------------------------------------------
# Task Models
# -----------------------------------------------------------------------------
class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., description="Task title (must start with capital letter)")
    description: Optional[str] = Field(default=None, description="Task description")
    priority: Literal["low", "medium", "high"] = Field(
        ..., description="Task priority level"
    )
    status: Literal["todo", "in_progress", "done"] = Field(
        ..., description="Current task status"
    )
    assigned_to: Optional[str] = Field(
        default=None, description="Username of assigned user"
    )

    @field_validator("title")
    @classmethod
    def title_must_start_with_capital(cls, v: str) -> str:
        """Validate that task title starts with an uppercase letter."""
        if not v or not v[0].isupper():
            raise ValueError("Title must start with a capital letter")
        return v


class Task(TaskCreate):
    """Task response model with generated id."""

    id: int = Field(..., description="Unique task identifier")
