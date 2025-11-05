"""Task class representing a single to-do item."""

from datetime import datetime
from typing import List, Optional
from my_todo_lib.core.constants import TaskStatus, Priority, DEFAULT_TASK_STATUS


class Task:
    """Represents a single to-do task with various properties.

    Attributes:
        id: Unique identifier for the task
        title: Task title/name
        description: Detailed description of the task
        status: Current status (todo, in_progress, completed)
        priority: Task priority level (low, medium, high)
        due_date: Optional due date for the task
        tags: List of tags for categorization
        created_at: Timestamp when task was created
        modified_at: Timestamp when task was last modified
    """

    _task_counter: int = 1  # Class variable for auto-incrementing IDs

    def __init__(
        self,
        title: str,
        description: str = "",
        status: TaskStatus = DEFAULT_TASK_STATUS,
        priority: Priority = Priority.MEDIUM,
        due_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        id_: Optional[int] = None,
    ):
        """Initialize a new Task.

        Args:
            title: Title of the task (required)
            description: Detailed description (optional)
            status: Task status (default: TODO)
            priority: Task priority (default: MEDIUM)
            due_date: Due date for the task (optional)
            tags: List of tags (optional)
            id_: Task ID (internal use for deserialization, optional)

        Raises:
            ValueError: If title is empty or exceeds max length
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        from my_todo_lib.core.constants import MAX_TASK_NAME_LENGTH

        if len(title) > MAX_TASK_NAME_LENGTH:
            raise ValueError(
                f"Task title exceeds max length of {MAX_TASK_NAME_LENGTH}"
            )

        # Use provided ID or generate new one
        if id_ is not None:
            self._id = id_
            # Update counter if necessary
            if id_ >= Task._task_counter:
                Task._task_counter = id_ + 1
        else:
            self._id = Task._task_counter
            Task._task_counter += 1

        self._title = title.strip()
        self._description = description.strip()
        self._status = status
        self._priority = priority
        self._due_date = due_date
        self._tags = tags if tags else []
        self._created_at = datetime.now()
        self._modified_at = datetime.now()

    @property
    def id(self) -> int:
        """Get the task ID."""
        return self._id

    @property
    def title(self) -> str:
        """Get the task title."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set the task title.

        Args:
            value: New title

        Raises:
            ValueError: If title is empty or exceeds max length
        """
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty")

        from my_todo_lib.core.constants import MAX_TASK_NAME_LENGTH

        if len(value) > MAX_TASK_NAME_LENGTH:
            raise ValueError(
                f"Task title exceeds max length of {MAX_TASK_NAME_LENGTH}"
            )

        self._title = value.strip()
        self._modified_at = datetime.now()

    @property
    def description(self) -> str:
        """Get the task description."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set the task description."""
        self._description = value.strip() if value else ""
        self._modified_at = datetime.now()

    @property
    def status(self) -> TaskStatus:
        """Get the task status."""
        return self._status

    @status.setter
    def status(self, value: TaskStatus) -> None:
        """Set the task status."""
        if not isinstance(value, TaskStatus):
            raise ValueError(f"Status must be a TaskStatus enum, got {type(value)}")
        self._status = value
        self._modified_at = datetime.now()

    @property
    def priority(self) -> Priority:
        """Get the task priority."""
        return self._priority

    @priority.setter
    def priority(self, value: Priority) -> None:
        """Set the task priority."""
        if not isinstance(value, Priority):
            raise ValueError(f"Priority must be a Priority enum, got {type(value)}")
        self._priority = value
        self._modified_at = datetime.now()

    @property
    def due_date(self) -> Optional[datetime]:
        """Get the task due date."""
        return self._due_date

    @due_date.setter
    def due_date(self, value: Optional[datetime]) -> None:
        """Set the task due date."""
        self._due_date = value
        self._modified_at = datetime.now()

    @property
    def tags(self) -> List[str]:
        """Get the task tags."""
        return self._tags.copy()

    def add_tag(self, tag: str) -> None:
        """Add a tag to the task.

        Args:
            tag: Tag to add

        Raises:
            ValueError: If tag is empty
        """
        if not tag or not tag.strip():
            raise ValueError("Tag cannot be empty")

        tag = tag.strip().lower()
        if tag not in self._tags:
            self._tags.append(tag)
            self._modified_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the task.

        Args:
            tag: Tag to remove
        """
        tag = tag.strip().lower()
        if tag in self._tags:
            self._tags.remove(tag)
            self._modified_at = datetime.now()

    @property
    def created_at(self) -> datetime:
        """Get the task creation timestamp."""
        return self._created_at

    @property
    def modified_at(self) -> datetime:
        """Get the task modification timestamp."""
        return self._modified_at

    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the task
        """
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "status": self._status.value,
            "priority": self._priority.value,
            "due_date": self._due_date.isoformat() if self._due_date else None,
            "tags": self._tags,
            "created_at": self._created_at.isoformat(),
            "modified_at": self._modified_at.isoformat(),
        }

    def __repr__(self) -> str:
        """Return string representation of the task."""
        return (
            f"Task(id={self._id}, title='{self._title}', "
            f"status={self._status.value}, priority={self._priority.value})"
        )

    def __eq__(self, other: object) -> bool:
        """Check if two tasks are equal based on ID."""
        if not isinstance(other, Task):
            return False
        return self._id == other._id
