"""
SQLAlchemy models for the Task Management System.
Database ORM models with validation.
"""

from datetime import datetime
from typing import Literal, Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    """SQLAlchemy model for User."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    role = Column(String(20), nullable=False)  # admin, manager, member
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TaskModel(Base):
    """SQLAlchemy model for Task."""
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="todo")  # todo, in_progress, done
    priority = Column(String(20), default="medium")  # low, medium, high
    assigned_to = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
