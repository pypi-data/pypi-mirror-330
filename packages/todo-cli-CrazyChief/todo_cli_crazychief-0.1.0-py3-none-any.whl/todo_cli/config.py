"""Configuration management for the TODO CLI application."""

import os
from pathlib import Path
from typing import Dict, Optional, Type

from .storage import JsonFileStorage, Storage


class StorageConfig:
    """Configuration for storage backends."""

    # Default storage settings
    DEFAULT_STORAGE_TYPE = "json"
    DEFAULT_STORAGE_PATH = str(Path.home() / ".todo" / "tasks.json")

    # Map of storage type identifiers to their implementations
    STORAGE_BACKENDS: Dict[str, Type[Storage]] = {
        "json": JsonFileStorage,
    }

    @classmethod
    def get_storage(cls) -> Storage:
        """Create and return a configured storage instance.

        The storage type and path can be configured using environment variables:
        - TODO_STORAGE_TYPE: Type of storage backend to use (default: 'json')
        - TODO_STORAGE_PATH: Path to the storage file/directory

        Returns:
            Configured storage instance
        """
        storage_type = os.getenv("TODO_STORAGE_TYPE", cls.DEFAULT_STORAGE_TYPE)
        storage_path = os.getenv("TODO_STORAGE_PATH", cls.DEFAULT_STORAGE_PATH)

        if storage_type not in cls.STORAGE_BACKENDS:
            raise ValueError(
                f"Unsupported storage type: {storage_type}. "
                f"Available types: {', '.join(cls.STORAGE_BACKENDS.keys())}"
            )

        storage_class = cls.STORAGE_BACKENDS[storage_type]
        return storage_class(storage_path)

    @classmethod
    def register_backend(cls, storage_type: str, storage_class: Type[Storage]) -> None:
        """Register a new storage backend.

        Args:
            storage_type: Identifier for the storage type
            storage_class: Storage implementation class
        """
        cls.STORAGE_BACKENDS[storage_type] = storage_class