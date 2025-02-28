# TODO CLI Technical Documentation

## Table of Contents
- [User Guide](#user-guide)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Adding Tasks](#adding-tasks)
    - [Listing Tasks](#listing-tasks)
    - [Completing Tasks](#completing-tasks)
    - [Deleting Tasks](#deleting-tasks)
- [Developer Guide](#developer-guide)
  - [Architecture](#architecture)
  - [Project Structure](#project-structure)
  - [Core Components](#core-components)
  - [Extending the Application](#extending-the-application)

## User Guide

### Installation

You can install the TODO CLI application using one of the following methods:

#### Method 1: Install from PyPI (Recommended for Users)

```bash
pip install todo-cli_CrazyChief
```

#### Method 2: Install from Source (Recommended for Developers)

1. Clone the repository:
```bash
git clone git@github.com:CrazyChief/todo-cli.git
cd todo_cli
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
```

This will install all required dependencies and the CLI tool. The `-e` flag installs the package in "editable" mode, which is useful for development.

#### System Requirements

- Python 3.6 or higher
- pip package manager

#### Verifying Installation

After installation, verify that the CLI tool is available:

```bash
todo --help
```

You should see the help message with available commands.

### Configuration

The TODO CLI application can be configured using environment variables:

- `TODO_STORAGE_TYPE`: Type of storage backend to use (default: 'json')
- `TODO_STORAGE_PATH`: Path to the storage file/directory (default: '~/.todo/tasks.json')

Example:
```bash
export TODO_STORAGE_PATH="/custom/path/tasks.json"
```

### Usage

#### Adding Tasks
```bash
todo add "Complete documentation" -d "Write user and developer guides"
```

#### Listing Tasks
```bash
todo list
```

#### Completing Tasks
```bash
todo complete <task-id>
```

#### Deleting Tasks
```bash
todo delete <task-id>
```

## Developer Guide

### Architecture

The application follows a layered architecture pattern:

1. **CLI Layer** (`cli.py`)
   - Handles command-line interface and user interaction
   - Uses Click for command parsing
   - Formats output using Rich library

2. **Service Layer** (`service.py`)
   - Implements business logic
   - Manages task operations
   - Coordinates between CLI and storage

3. **Storage Layer** (`storage.py`)
   - Handles data persistence
   - Provides abstract interface for storage backends
   - Includes JSON file implementation

### Project Structure

```
todo_cli/
├── todo_cli/
│   ├── __init__.py
│   ├── cli.py        # Command-line interface
│   ├── config.py     # Configuration management
│   ├── models.py     # Data models
│   ├── service.py    # Business logic
│   └── storage.py    # Storage implementations
├── requirements.txt
└── docs/
    └── README.md
```

### Core Components

#### Models

The `Task` model (`models.py`) represents a todo item with the following attributes:
- `id`: Unique identifier
- `title`: Task title
- `description`: Optional task description
- `status`: Task status (OPEN/COMPLETED)
- `created_at`: Creation timestamp
- `completed_at`: Completion timestamp

#### Storage System

The storage system is designed to be extensible:

1. Abstract Base Class (`Storage`):
```python
class Storage(ABC):
    @abstractmethod
    def add_task(self, task: Task) -> None: pass
    @abstractmethod
    def get_task(self, task_id: str) -> Optional[Task]: pass
    @abstractmethod
    def list_tasks(self) -> List[Task]: pass
    @abstractmethod
    def update_task(self, task: Task) -> None: pass
    @abstractmethod
    def delete_task(self, task_id: str) -> None: pass
```

2. JSON File Implementation (`JsonFileStorage`):
- Stores tasks in a JSON file
- Handles file creation and data serialization
- Thread-safe file operations

### Extending the Application

#### Adding a New Storage Backend

1. Create a new class implementing the `Storage` interface:
```python
from todo_cli.storage import Storage

class MyCustomStorage(Storage):
    def __init__(self, connection_string: str):
        # Initialize your storage
        pass

    def add_task(self, task: Task) -> None:
        # Implement task creation
        pass

    # Implement other required methods
```

2. Register the backend in `config.py`:
```python
from todo_cli.config import StorageConfig
StorageConfig.register_backend("custom", MyCustomStorage)
```

#### Adding New Commands

1. Add a new command in `cli.py`:
```python
@cli.command()
@click.argument("arg_name")
@click.option("--option-name", help="Option description")
def new_command(arg_name: str, option_name: str):
    """Command description."""
    service = get_service()
    # Implement command logic
```

2. Add corresponding service method in `service.py`:
```python
def new_service_method(self, param: str) -> Result:
    # Implement service logic
    pass
```

#### Error Handling

The application uses standard Python exceptions for error handling:
- `KeyError`: For not found errors
- `ValueError`: For validation errors
- Custom exceptions can be added for specific cases

#### Testing

To run tests:
```bash
python -m pytest tests/
```

When adding new features:
1. Write unit tests for new components
2. Ensure existing tests pass
3. Update documentation as needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

Please follow the existing code style and include appropriate documentation updates.