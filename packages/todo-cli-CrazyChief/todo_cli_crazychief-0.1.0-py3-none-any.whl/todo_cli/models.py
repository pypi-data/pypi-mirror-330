"""Data models for the TODO CLI application."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Enumeration of possible task statuses."""
    OPEN = PENDING = "open"
    COMPLETED = "completed"


class Task(BaseModel):
    """Represents a single task in the TODO list."""
    id: str = Field(..., description="Unique identifier for the task")
    title: str = Field(..., description="Title of the task")
    description: Optional[str] = Field(None, description="Optional description of the task")
    status: TaskStatus = Field(default=TaskStatus.OPEN, description="Current status of the task")
    created_at: datetime = Field(default_factory=datetime.now, description="Task creation timestamp")
    completed_at: Optional[datetime] = Field(None, description="Task completion timestamp")