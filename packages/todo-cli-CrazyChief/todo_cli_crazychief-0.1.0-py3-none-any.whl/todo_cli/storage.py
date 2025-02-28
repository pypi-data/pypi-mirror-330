"""Storage implementations for the TODO CLI application."""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import TypeAdapter

from .models import Task


class Storage(ABC):
    """Abstract base class for task storage implementations."""

    @abstractmethod
    def add_task(self, task: Task) -> None:
        """Add a new task to storage."""
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID."""
        pass

    @abstractmethod
    def list_tasks(self) -> List[Task]:
        """List all tasks in storage."""
        pass

    @abstractmethod
    def update_task(self, task: Task) -> None:
        """Update an existing task."""
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> None:
        """Delete a task by its ID."""
        pass


class JsonFileStorage(Storage):
    """JSON file-based implementation of task storage."""

    def __init__(self, file_path: str = None):
        """Initialize JSON file storage.

        Args:
            file_path: Path to the JSON file. Defaults to ~/.todo/tasks.json
        """
        if file_path is None:
            file_path = str(Path.home() / ".todo" / "tasks.json")
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create the storage file if it doesn't exist."""
        if not self.file_path.exists():
            self.file_path.write_text("[]")

    def _load_tasks(self) -> List[Task]:
        """Load all tasks from the JSON file."""
        content = self.file_path.read_text()
        if not content:
            return []
        
        raw_data = json.loads(content)
        task_adapter = TypeAdapter(List[Task])
        return task_adapter.validate_python(raw_data)

    def _save_tasks(self, tasks: List[Task]) -> None:
        """Save tasks to the JSON file."""
        task_list = [task.model_dump() for task in tasks]
        self.file_path.write_text(json.dumps(task_list, default=str, indent=2))

    def add_task(self, task: Task) -> None:
        tasks = self._load_tasks()
        tasks.append(task)
        self._save_tasks(tasks)

    def get_task(self, task_id: str) -> Optional[Task]:
        tasks = self._load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def list_tasks(self) -> List[Task]:
        return self._load_tasks()

    def update_task(self, task: Task) -> None:
        tasks = self._load_tasks()
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task
                self._save_tasks(tasks)
                return
        raise KeyError(f"Task with ID {task.id} not found")

    def delete_task(self, task_id: str) -> None:
        tasks = self._load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                tasks.pop(i)
                self._save_tasks(tasks)
                return
        raise KeyError(f"Task with ID {task_id} not found")