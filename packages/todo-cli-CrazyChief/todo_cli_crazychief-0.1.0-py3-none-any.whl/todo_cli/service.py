"""Service layer for the TODO CLI application."""

import uuid
from datetime import datetime
from typing import List, Optional

from .models import Task, TaskStatus
from .storage import Storage


class TodoService:
    """Service class for managing TODO tasks."""

    def __init__(self, storage: Storage):
        """Initialize the TODO service.

        Args:
            storage: Storage implementation to use for task persistence
        """
        self.storage = storage

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """Create a new task.

        Args:
            title: Title of the task
            description: Optional description of the task

        Returns:
            The created task
        """
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description
        )
        self.storage.add_task(task)
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        return self.storage.get_task(task_id)

    def list_tasks(self) -> List[Task]:
        """List all tasks.

        Returns:
            List of all tasks
        """
        return self.storage.list_tasks()

    def complete_task(self, task_id: str) -> Task:
        """Mark a task as completed.

        Args:
            task_id: ID of the task to complete

        Returns:
            The updated task

        Raises:
            KeyError: If the task is not found
        """
        task = self.storage.get_task(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found")

        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        self.storage.update_task(task)
        return task

    def delete_task(self, task_id: str) -> None:
        """Delete a task.

        Args:
            task_id: ID of the task to delete

        Raises:
            KeyError: If the task is not found
        """
        self.storage.delete_task(task_id)