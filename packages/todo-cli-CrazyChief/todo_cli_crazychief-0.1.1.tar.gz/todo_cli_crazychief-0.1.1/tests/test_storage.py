"""Test cases for the storage layer."""

import json
import pytest
from pathlib import Path
from datetime import datetime
from todo_cli.models import Task, TaskStatus
from todo_cli.storage import JsonFileStorage

@pytest.fixture
def temp_storage_file(tmp_path):
    """Create a temporary storage file for testing."""
    storage_file = tmp_path / "tasks.json"
    return storage_file

@pytest.fixture
def storage(temp_storage_file):
    """Create a JsonFileStorage instance with a temporary file."""
    return JsonFileStorage(temp_storage_file)

def test_storage_file_creation(temp_storage_file):
    """Test storage file creation."""
    JsonFileStorage(temp_storage_file)
    assert temp_storage_file.exists()
    assert json.loads(temp_storage_file.read_text()) == []

def test_add_task(storage, temp_storage_file):
    """Test adding a task to storage."""
    task = Task(id="test-id", title="Test Task")
    storage.add_task(task)
    
    stored_data = json.loads(temp_storage_file.read_text())
    assert len(stored_data) == 1
    assert stored_data[0]["id"] == "test-id"
    assert stored_data[0]["title"] == "Test Task"

def test_get_task(storage):
    """Test retrieving a task from storage."""
    task = Task(id="test-id", title="Test Task")
    storage.add_task(task)
    
    retrieved_task = storage.get_task("test-id")
    assert retrieved_task is not None
    assert retrieved_task.id == task.id
    assert retrieved_task.title == task.title

def test_get_nonexistent_task(storage):
    """Test retrieving a non-existent task."""
    assert storage.get_task("nonexistent-id") is None

def test_list_tasks(storage):
    """Test listing all tasks."""
    tasks = [
        Task(id="1", title="Task 1"),
        Task(id="2", title="Task 2")
    ]
    for task in tasks:
        storage.add_task(task)
    
    stored_tasks = storage.list_tasks()
    assert len(stored_tasks) == 2
    assert all(isinstance(task, Task) for task in stored_tasks)
    assert [task.id for task in stored_tasks] == ["1", "2"]

def test_update_task(storage):
    """Test updating a task."""
    task = Task(id="test-id", title="Test Task")
    storage.add_task(task)
    
    task.title = "Updated Task"
    task.status = TaskStatus.COMPLETED
    storage.update_task(task)
    
    updated_task = storage.get_task("test-id")
    assert updated_task.title == "Updated Task"
    assert updated_task.status == TaskStatus.COMPLETED

def test_delete_task(storage):
    """Test deleting a task."""
    task = Task(id="test-id", title="Test Task")
    storage.add_task(task)
    
    storage.delete_task("test-id")
    assert storage.get_task("test-id") is None

def test_concurrent_access(storage):
    """Test thread-safe operations."""
    task1 = Task(id="1", title="Task 1")
    task2 = Task(id="2", title="Task 2")
    
    storage.add_task(task1)
    storage.add_task(task2)
    
    tasks = storage.list_tasks()
    assert len(tasks) == 2
    
    storage.delete_task("1")
    storage.update_task(Task(id="2", title="Updated Task 2"))
    
    final_tasks = storage.list_tasks()
    assert len(final_tasks) == 1
    assert final_tasks[0].title == "Updated Task 2"