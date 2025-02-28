"""Test cases for the service layer."""

import pytest
from unittest.mock import Mock
from datetime import datetime
from todo_cli.models import Task, TaskStatus
from todo_cli.service import TodoService

@pytest.fixture
def mock_storage():
    """Create a mock storage implementation."""
    return Mock()

@pytest.fixture
def todo_service(mock_storage):
    """Create a TodoService instance with mock storage."""
    return TodoService(mock_storage)

def test_create_task(todo_service, mock_storage):
    """Test task creation."""
    task = todo_service.create_task("Test Task", "Test Description")
    
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == TaskStatus.PENDING
    mock_storage.add_task.assert_called_once_with(task)

def test_get_task(todo_service, mock_storage):
    """Test task retrieval."""
    mock_task = Task(id="test-id", title="Test Task")
    mock_storage.get_task.return_value = mock_task
    
    task = todo_service.get_task("test-id")
    
    assert task == mock_task
    mock_storage.get_task.assert_called_once_with("test-id")

def test_list_tasks(todo_service, mock_storage):
    """Test listing all tasks."""
    mock_tasks = [
        Task(id="1", title="Task 1"),
        Task(id="2", title="Task 2")
    ]
    mock_storage.list_tasks.return_value = mock_tasks
    
    tasks = todo_service.list_tasks()
    
    assert tasks == mock_tasks
    mock_storage.list_tasks.assert_called_once()

def test_complete_task(todo_service, mock_storage):
    """Test task completion."""
    mock_task = Task(id="test-id", title="Test Task")
    mock_storage.get_task.return_value = mock_task
    
    task = todo_service.complete_task("test-id")
    
    assert task.status == TaskStatus.COMPLETED
    assert task.completed_at is not None
    mock_storage.update_task.assert_called_once_with(task)

def test_complete_nonexistent_task(todo_service, mock_storage):
    """Test completing a non-existent task."""
    mock_storage.get_task.return_value = None
    
    with pytest.raises(KeyError):
        todo_service.complete_task("nonexistent-id")

def test_delete_task(todo_service, mock_storage):
    """Test task deletion."""
    todo_service.delete_task("test-id")
    mock_storage.delete_task.assert_called_once_with("test-id")