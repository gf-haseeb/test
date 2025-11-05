"""TaskManager - Main orchestrator for the to-do library."""

from datetime import datetime
from typing import List, Optional
from my_todo_lib.core.list_container import ListContainer
from my_todo_lib.core.task_list import TaskList
from my_todo_lib.core.task import Task
from my_todo_lib.core.constants import (
    OrderingStrategy,
    TaskStatus,
    Priority,
    DEFAULT_TASK_STATUS,
)
from my_todo_lib.storage.base import Storage
from my_todo_lib.storage.json_storage import JSONStorage


class TaskManager:
    """Main API for managing tasks and lists.

    TaskManager coordinates between the core components (Task, TaskList,
    ListContainer) and storage backends to provide a unified interface
    for users of the library.

    Attributes:
        container: ListContainer managing all lists
        storage: Storage backend for persistence
    """

    def __init__(self, storage: Optional[Storage] = None):
        """Initialize TaskManager with optional storage.

        Args:
            storage: Storage backend to use (default: JSONStorage with tasks.json)
        """
        self._container = ListContainer()
        self._storage = storage if storage else JSONStorage("tasks.json")

    @property
    def container(self) -> ListContainer:
        """Get the internal ListContainer."""
        return self._container

    @property
    def storage(self) -> Storage:
        """Get the storage backend."""
        return self._storage

    # ============= List Management =============

    def create_list(
        self,
        name: str,
        description: str = "",
    ) -> TaskList:
        """Create a new task list.

        Args:
            name: Name of the new list
            description: Description of the new list (optional)

        Returns:
            The created TaskList object

        Raises:
            ValueError: If name is invalid
        """
        task_list = self._container.create_list(name, description)
        self.save()
        return task_list

    def get_lists(self) -> List[TaskList]:
        """Get all lists sorted by current ordering strategy.

        Returns:
            List of TaskList objects in sorted order
        """
        return self._container.get_lists()

    def get_list(self, list_id: int) -> Optional[TaskList]:
        """Get a specific list by ID.

        Args:
            list_id: ID of the list to retrieve

        Returns:
            TaskList if found, None otherwise
        """
        return self._container.get_list(list_id)

    def delete_list(self, list_id: int) -> None:
        """Delete a list by ID.

        Args:
            list_id: ID of the list to delete

        Raises:
            ValueError: If list not found
        """
        result = self._container.remove_list(list_id)
        if not result:
            raise ValueError(f"List with ID {list_id} not found")
        self.save()

    def rename_list(self, list_id: int, new_name: str) -> None:
        """Rename a list.

        Args:
            list_id: ID of the list to rename
            new_name: New name for the list

        Raises:
            ValueError: If list not found or new_name invalid
        """
        self._container.rename_list(list_id, new_name)
        self.save()

    def set_list_ordering(self, strategy: OrderingStrategy) -> None:
        """Set how lists are ordered.

        Args:
            strategy: OrderingStrategy to apply

        Raises:
            ValueError: If strategy is invalid
        """
        self._container.set_ordering_strategy(strategy)
        self.save()

    def move_list(self, list_id: int, position: int) -> None:
        """Move a list to a new position (MANUAL strategy only).

        Args:
            list_id: ID of the list to move
            position: Target position (0-indexed)

        Raises:
            ValueError: If strategy is not MANUAL or parameters invalid
        """
        self._container.move_list(list_id, position)
        self.save()

    # ============= Task Management =============

    def add_task_to_list(
        self,
        list_id: int,
        title: str,
        description: str = "",
        status: TaskStatus = DEFAULT_TASK_STATUS,
        priority: Priority = Priority.MEDIUM,
        due_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
    ) -> Task:
        """Add a task to a specific list.

        Args:
            list_id: ID of the list
            title: Task title (required)
            description: Task description (optional)
            status: Task status (default: TODO)
            priority: Task priority (default: MEDIUM)
            due_date: Due date for task (optional)
            tags: List of tags (optional)

        Returns:
            Created Task object

        Raises:
            ValueError: If list not found
        """
        task_list = self.get_list(list_id)
        if task_list is None:
            raise ValueError(f"List with ID {list_id} not found")

        task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            tags=tags,
        )
        task_list.add_task(task)
        self.save()
        return task

    def get_task(self, list_id: int, task_id: int) -> Optional[Task]:
        """Get a specific task from a list.

        Args:
            list_id: ID of the list
            task_id: ID of the task

        Returns:
            Task if found, None otherwise
        """
        task_list = self.get_list(list_id)
        if task_list is None:
            return None

        return task_list.get_task(task_id)

    def get_tasks(
        self,
        list_id: int,
        status: Optional[TaskStatus] = None,
        sort_by: str = "created_at",
    ) -> List[Task]:
        """Get tasks from a list with optional filtering.

        Args:
            list_id: ID of the list
            status: Optional status filter
            sort_by: Field to sort by (created_at, modified_at, priority)

        Returns:
            Filtered and sorted list of tasks

        Raises:
            ValueError: If list not found or parameters invalid
        """
        task_list = self.get_list(list_id)
        if task_list is None:
            raise ValueError(f"List with ID {list_id} not found")

        return task_list.get_tasks(status=status, sort_by=sort_by)

    def update_task(
        self,
        list_id: int,
        task_id: int,
        **kwargs,
    ) -> None:
        """Update task properties.

        Args:
            list_id: ID of the list
            task_id: ID of the task
            **kwargs: Properties to update (title, description, status, priority, etc.)

        Raises:
            ValueError: If list or task not found
        """
        task = self.get_task(list_id, task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found in list {list_id}")

        # Update allowed properties
        allowed_props = {
            "title", "description", "status", "priority", "due_date"
        }
        for key, value in kwargs.items():
            if key not in allowed_props:
                raise ValueError(f"Cannot update property: {key}")
            setattr(task, key, value)

        self.save()

    def delete_task(self, list_id: int, task_id: int) -> bool:
        """Delete a task from a list.

        Args:
            list_id: ID of the list
            task_id: ID of the task

        Returns:
            True if deleted, False if not found

        Raises:
            ValueError: If list not found
        """
        task_list = self.get_list(list_id)
        if task_list is None:
            raise ValueError(f"List with ID {list_id} not found")

        result = task_list.remove_task(task_id)
        if result:
            self.save()
        return result

    def move_task_to_list(
        self,
        source_list_id: int,
        task_id: int,
        target_list_id: int,
    ) -> Task:
        """Move a task from one list to another.

        Args:
            source_list_id: ID of the source list (where task currently is)
            task_id: ID of the task to move
            target_list_id: ID of the target list (where task will go)

        Returns:
            The moved Task object

        Raises:
            ValueError: If source list, target list, or task not found
        """
        # Get source list
        source_list = self.get_list(source_list_id)
        if source_list is None:
            raise ValueError(f"Source list with ID {source_list_id} not found")

        # Get target list
        target_list = self.get_list(target_list_id)
        if target_list is None:
            raise ValueError(f"Target list with ID {target_list_id} not found")

        # Cannot move task to same list
        if source_list_id == target_list_id:
            raise ValueError("Source and target lists cannot be the same")

        # Get the task from source list
        task = source_list.get_task(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found in source list")

        # Remove task from source list
        source_list.remove_task(task_id)

        # Add task to target list
        target_list.add_task(task)

        # Save changes
        self.save()

        return task

    def search_tasks_across_lists(
        self,
        query: str,
        search_in: str = "title",
    ) -> List[tuple]:
        """Search for tasks across all lists.

        Args:
            query: Search query string (case-insensitive)
            search_in: Field to search (title, description, tags)

        Returns:
            List of tuples (TaskList, Task) matching the query

        Raises:
            ValueError: If search_in field is invalid
        """
        valid_fields = {"title", "description", "tags"}
        if search_in not in valid_fields:
            raise ValueError(
                f"search_in must be one of {valid_fields}, got {search_in}"
            )

        results = []
        query_lower = query.lower()

        for task_list in self._container.get_all_lists():
            for task in task_list.get_all_tasks():
                if search_in == "title":
                    if query_lower in task.title.lower():
                        results.append((task_list, task))
                elif search_in == "description":
                    if query_lower in task.description.lower():
                        results.append((task_list, task))
                elif search_in == "tags":
                    if any(query_lower in tag.lower() for tag in task.tags):
                        results.append((task_list, task))

        return results

    # ============= Persistence =============

    def save(self) -> None:
        """Save all data to storage.

        Raises:
            IOError: If save operation fails
        """
        try:
            self._storage.save(self._container)
        except Exception as e:
            raise IOError(f"Failed to save data: {str(e)}")

    def load(self) -> None:
        """Load all data from storage.

        Replaces current container with loaded data.

        Raises:
            ValueError: If stored data is invalid
            IOError: If load operation fails
        """
        try:
            self._container = self._storage.load()
        except Exception as e:
            raise IOError(f"Failed to load data: {str(e)}")

    def clear(self) -> None:
        """Clear all data from storage and reset container.

        Raises:
            IOError: If clear operation fails
        """
        self._storage.clear()
        self._container = ListContainer()

    # ============= Statistics =============

    def get_statistics(self) -> dict:
        """Get statistics about tasks and lists.

        Returns:
            Dictionary with statistics
        """
        total_lists = self._container.list_count
        total_tasks = 0
        completed_tasks = 0
        todo_tasks = 0
        in_progress_tasks = 0

        for task_list in self._container.get_all_lists():
            all_tasks = task_list.get_all_tasks()
            total_tasks += len(all_tasks)

            for task in all_tasks:
                if task.status == TaskStatus.COMPLETED:
                    completed_tasks += 1
                elif task.status == TaskStatus.TODO:
                    todo_tasks += 1
                elif task.status == TaskStatus.IN_PROGRESS:
                    in_progress_tasks += 1

        completion_percentage = (
            (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        )

        return {
            "total_lists": total_lists,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "todo_tasks": todo_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completion_percentage": round(completion_percentage, 2),
        }

    def __repr__(self) -> str:
        """Return string representation of TaskManager."""
        stats = self.get_statistics()
        return (
            f"TaskManager(lists={stats['total_lists']}, "
            f"tasks={stats['total_tasks']}, "
            f"completed={stats['completed_tasks']})"
        )
