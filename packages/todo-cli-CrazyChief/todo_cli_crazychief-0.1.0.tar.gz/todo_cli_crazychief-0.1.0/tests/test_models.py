"""Test cases for the models module."""

import pytest
from datetime import datetime
from todo_cli.models import Task, TaskStatus

def test_task_creation():
    """Test basic task creation."""
    task = Task(
        id="test-id",
        title="Test Task",
        description="Test Description"
    )
    assert task.id == "test-id"
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == TaskStatus.PENDING
    assert task.created_at is not None
    assert task.completed_at is None

def test_task_completion():
    """Test task completion functionality."""
    task = Task(
        id="test-id",
        title="Test Task"
    )
    assert task.status == TaskStatus.PENDING
    
    task.status = TaskStatus.COMPLETED
    task.completed_at = datetime.now()
    
    assert task.status == TaskStatus.COMPLETED
    assert task.completed_at is not None

def test_task_optional_description():
    """Test task creation without description."""
    task = Task(
        id="test-id",
        title="Test Task"
    )
    assert task.description is None

def test_task_status_enum():
    """Test TaskStatus enumeration values."""
    assert TaskStatus.PENDING.value == "open"
    assert TaskStatus.COMPLETED.value == "completed"
    
    with pytest.raises(ValueError):
        Task(id="test-id", title="Test Task", status="invalid")