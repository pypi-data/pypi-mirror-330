"""Command-line interface for the TODO CLI application."""

from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from .models import TaskStatus
from .service import TodoService
from .storage import JsonFileStorage

console = Console()


def get_service() -> TodoService:
    """Create and return a TodoService instance with configured storage."""
    from .config import StorageConfig
    return TodoService(StorageConfig.get_storage())


def format_task_table(tasks) -> Table:
    """Create a rich table for displaying tasks."""
    table = Table(show_header=True)
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Status")
    table.add_column("Created")
    table.add_column("Completed")

    for task in tasks:
        completed_at = task.completed_at.strftime("%Y-%m-%d %H:%M") if task.completed_at else "-"
        table.add_row(
            task.id,
            task.title,
            task.description or "-",
            task.status.value,
            task.created_at.strftime("%Y-%m-%d %H:%M"),
            completed_at,
            style="dim" if task.status == TaskStatus.COMPLETED else ""
        )

    return table


@click.group()
def cli():
    """A simple command-line TODO list manager."""
    pass


@cli.command()
@click.argument("title")
@click.option("-d", "--description", help="Optional task description")
def add(title: str, description: Optional[str]):
    """Add a new task with the given title and optional description."""
    service = get_service()
    task = service.create_task(title, description)
    console.print(f"✅ Created task: {task.title} (ID: {task.id})")


@cli.command()
def list():
    """List all tasks."""
    service = get_service()
    tasks = service.list_tasks()
    if not tasks:
        console.print("No tasks found.")
        return

    table = format_task_table(tasks)
    console.print(table)


@cli.command()
@click.argument("task_id")
def complete(task_id: str):
    """Mark a task as completed."""
    service = get_service()
    try:
        task = service.complete_task(task_id)
        console.print(f"✅ Marked task as completed: {task.title}")
    except KeyError as e:
        console.print(f"❌ Error: {str(e)}", style="red")


@cli.command()
@click.argument("task_id")
def delete(task_id: str):
    """Delete a task."""
    service = get_service()
    try:
        service.delete_task(task_id)
        console.print(f"✅ Deleted task with ID: {task_id}")
    except KeyError as e:
        console.print(f"❌ Error: {str(e)}", style="red")


if __name__ == "__main__":
    cli()