"""TaskList class representing a collection of tasks."""

from datetime import datetime
from typing import List, Optional
from my_todo_lib.core.task import Task
from my_todo_lib.core.constants import TaskStatus, MAX_LIST_NAME_LENGTH


class TaskList:
    """Represents a single list containing multiple tasks.

    Attributes:
        id: Unique identifier for the list
        name: Name of the list
        description: Description of the list
        tasks: Collection of Task objects
        created_at: Timestamp when list was created
        modified_at: Timestamp when list was last modified
    """

    _list_counter: int = 1  # Class variable for auto-incrementing IDs

    def __init__(
        self,
        name: str,
        description: str = "",
        id_: Optional[int] = None,
    ):
        """Initialize a new TaskList.

        Args:
            name: Name of the list (required)
            description: Description of the list (optional)
            id_: List ID (internal use for deserialization, optional)

        Raises:
            ValueError: If name is empty or exceeds max length
        """
        if not name or not name.strip():
            raise ValueError("List name cannot be empty")

        if len(name) > MAX_LIST_NAME_LENGTH:
            raise ValueError(
                f"List name exceeds max length of {MAX_LIST_NAME_LENGTH}"
            )

        # Use provided ID or generate new one
        if id_ is not None:
            self._id = id_
            # Update counter if necessary
            if id_ >= TaskList._list_counter:
                TaskList._list_counter = id_ + 1
        else:
            self._id = TaskList._list_counter
            TaskList._list_counter += 1

        self._name = name.strip()
        self._description = description.strip()
        self._tasks: List[Task] = []
        self._created_at = datetime.now()
        self._modified_at = datetime.now()

    @property
    def id(self) -> int:
        """Get the list ID."""
        return self._id

    @property
    def name(self) -> str:
        """Get the list name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the list name.

        Args:
            value: New name

        Raises:
            ValueError: If name is empty or exceeds max length
        """
        if not value or not value.strip():
            raise ValueError("List name cannot be empty")

        if len(value) > MAX_LIST_NAME_LENGTH:
            raise ValueError(
                f"List name exceeds max length of {MAX_LIST_NAME_LENGTH}"
            )

        self._name = value.strip()
        self._modified_at = datetime.now()

    @property
    def description(self) -> str:
        """Get the list description."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set the list description."""
        self._description = value.strip() if value else ""
        self._modified_at = datetime.now()

    @property
    def created_at(self) -> datetime:
        """Get the list creation timestamp."""
        return self._created_at

    @property
    def modified_at(self) -> datetime:
        """Get the list modification timestamp."""
        return self._modified_at

    @property
    def task_count(self) -> int:
        """Get the number of tasks in the list."""
        return len(self._tasks)

    def add_task(self, task: Task) -> None:
        """Add a task to the list.

        Args:
            task: Task object to add

        Raises:
            ValueError: If task is already in the list
            TypeError: If task is not a Task instance
        """
        if not isinstance(task, Task):
            raise TypeError(f"Expected Task instance, got {type(task)}")

        if task in self._tasks:
            raise ValueError(f"Task '{task.title}' already exists in this list")

        self._tasks.append(task)
        self._modified_at = datetime.now()

    def remove_task(self, task_id: int) -> bool:
        """Remove a task from the list by ID.

        Args:
            task_id: ID of the task to remove

        Returns:
            True if task was removed, False if not found
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                self._modified_at = datetime.now()
                return True
        return False

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def get_tasks(
        self,
        status: Optional[TaskStatus] = None,
        sort_by: str = "created_at",
    ) -> List[Task]:
        """Get all tasks with optional filtering and sorting.

        Args:
            status: Optional status filter (todo, in_progress, completed)
            sort_by: Field to sort by (created_at, modified_at, priority)

        Returns:
            Filtered and sorted list of tasks

        Raises:
            ValueError: If sort_by field is invalid
        """
        # Filter by status if provided
        filtered_tasks = self._tasks
        if status is not None:
            if not isinstance(status, TaskStatus):
                raise ValueError(
                    f"Status must be TaskStatus enum, got {type(status)}"
                )
            filtered_tasks = [t for t in self._tasks if t.status == status]

        # Sort by the specified field
        valid_sort_fields = ["created_at", "modified_at", "priority"]
        if sort_by not in valid_sort_fields:
            raise ValueError(
                f"sort_by must be one of {valid_sort_fields}, got {sort_by}"
            )

        if sort_by == "created_at":
            return sorted(filtered_tasks, key=lambda t: t.created_at)
        elif sort_by == "modified_at":
            return sorted(filtered_tasks, key=lambda t: t.modified_at)
        elif sort_by == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            return sorted(
                filtered_tasks,
                key=lambda t: priority_order[t.priority.value],
            )

        return filtered_tasks

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks in the list without filtering.

        Returns:
            List of all tasks
        """
        return self._tasks.copy()

    def clear_completed_tasks(self) -> int:
        """Remove all completed tasks from the list.

        Returns:
            Number of tasks removed
        """
        initial_count = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.status != TaskStatus.COMPLETED]
        removed_count = initial_count - len(self._tasks)
        if removed_count > 0:
            self._modified_at = datetime.now()
        return removed_count

    def to_dict(self) -> dict:
        """Convert task list to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the task list
        """
        return {
            "id": self._id,
            "name": self._name,
            "description": self._description,
            "created_at": self._created_at.isoformat(),
            "modified_at": self._modified_at.isoformat(),
            "tasks": [task.to_dict() for task in self._tasks],
        }

    def __repr__(self) -> str:
        """Return string representation of the task list."""
        return (
            f"TaskList(id={self._id}, name='{self._name}', "
            f"task_count={self.task_count})"
        )

    def __eq__(self, other: object) -> bool:
        """Check if two task lists are equal based on ID."""
        if not isinstance(other, TaskList):
            return False
        return self._id == other._id
