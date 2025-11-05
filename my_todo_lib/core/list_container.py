"""ListContainer class managing multiple task lists with ordering."""

from datetime import datetime
from typing import List, Optional, Tuple
from my_todo_lib.core.task_list import TaskList
from my_todo_lib.core.ordering import OrderingStrategy, OrderingStrategies
from my_todo_lib.core.constants import DEFAULT_ORDERING_STRATEGY


class ListContainer:
    """Manages multiple TaskList objects with flexible ordering strategies.

    Attributes:
        lists: Collection of TaskList objects
        ordering_strategy: Current strategy for ordering lists
        metadata: Additional metadata for lists (e.g., custom ordering indices)
    """

    def __init__(
        self,
        ordering_strategy: OrderingStrategy = DEFAULT_ORDERING_STRATEGY,
    ):
        """Initialize a new ListContainer.

        Args:
            ordering_strategy: Strategy for ordering lists (default: MANUAL)
        """
        if not isinstance(ordering_strategy, OrderingStrategy):
            raise ValueError(
                f"ordering_strategy must be OrderingStrategy enum, "
                f"got {type(ordering_strategy)}"
            )

        self._lists: List[TaskList] = []
        self._ordering_strategy = ordering_strategy
        self._metadata: dict = {}  # Stores metadata like custom_index per list
        self._created_at = datetime.now()
        self._modified_at = datetime.now()

    @property
    def ordering_strategy(self) -> OrderingStrategy:
        """Get the current ordering strategy."""
        return self._ordering_strategy

    def set_ordering_strategy(self, strategy: OrderingStrategy) -> None:
        """Set a new ordering strategy.

        Args:
            strategy: New OrderingStrategy to use

        Raises:
            ValueError: If strategy is not an OrderingStrategy enum
        """
        if not isinstance(strategy, OrderingStrategy):
            raise ValueError(
                f"strategy must be OrderingStrategy enum, got {type(strategy)}"
            )

        self._ordering_strategy = strategy
        self._modified_at = datetime.now()

    @property
    def list_count(self) -> int:
        """Get the number of lists in the container."""
        return len(self._lists)

    def create_list(
        self,
        name: str,
        description: str = "",
    ) -> TaskList:
        """Create and add a new TaskList to the container.

        Args:
            name: Name of the new list
            description: Description of the new list (optional)

        Returns:
            The created TaskList object

        Raises:
            ValueError: If name is invalid
        """
        task_list = TaskList(name=name, description=description)
        self._lists.append(task_list)

        # Initialize metadata for this list
        self._metadata[task_list.id] = {
            "custom_index": len(self._lists) - 1,
            "created_at": datetime.now(),
        }

        self._modified_at = datetime.now()
        return task_list

    def add_list(self, task_list: TaskList) -> None:
        """Add an existing TaskList to the container.

        Args:
            task_list: TaskList object to add

        Raises:
            TypeError: If task_list is not a TaskList instance
            ValueError: If list already exists in container
        """
        if not isinstance(task_list, TaskList):
            raise TypeError(f"Expected TaskList instance, got {type(task_list)}")

        if task_list in self._lists:
            raise ValueError(
                f"List '{task_list.name}' already exists in this container"
            )

        self._lists.append(task_list)

        # Initialize metadata for this list
        self._metadata[task_list.id] = {
            "custom_index": len(self._lists) - 1,
            "created_at": datetime.now(),
        }

        self._modified_at = datetime.now()

    def remove_list(self, list_id: int) -> bool:
        """Remove a list from the container by ID.

        Args:
            list_id: ID of the list to remove

        Returns:
            True if list was removed, False if not found
        """
        for i, task_list in enumerate(self._lists):
            if task_list.id == list_id:
                self._lists.pop(i)
                if list_id in self._metadata:
                    del self._metadata[list_id]
                self._modified_at = datetime.now()
                return True
        return False

    def get_list(self, list_id: int) -> Optional[TaskList]:
        """Get a list by ID.

        Args:
            list_id: ID of the list to retrieve

        Returns:
            TaskList object if found, None otherwise
        """
        for task_list in self._lists:
            if task_list.id == list_id:
                return task_list
        return None

    def get_lists(self) -> List[TaskList]:
        """Get all lists sorted by current ordering strategy.

        Returns:
            List of TaskList objects sorted by current strategy
        """
        if not self._lists:
            return []

        strategy_func = OrderingStrategies.get_strategy(self._ordering_strategy)
        return strategy_func(self._lists, self._metadata)

    def get_all_lists(self) -> List[TaskList]:
        """Get all lists without applying ordering strategy.

        Returns:
            Copy of all TaskList objects in creation order
        """
        return self._lists.copy()

    def move_list(self, list_id: int, position: int) -> None:
        """Reorder a list to a new position (MANUAL strategy only).

        Args:
            list_id: ID of the list to move
            position: Target position (0-indexed)

        Raises:
            ValueError: If strategy is not MANUAL
            ValueError: If list_id doesn't exist
            ValueError: If position is invalid
        """
        if self._ordering_strategy != OrderingStrategy.MANUAL:
            raise ValueError(
                "move_list() only works with MANUAL ordering strategy"
            )

        list_index = None
        for i, task_list in enumerate(self._lists):
            if task_list.id == list_id:
                list_index = i
                break

        if list_index is None:
            raise ValueError(f"List with ID {list_id} not found")

        if position < 0 or position >= len(self._lists):
            raise ValueError(
                f"Position must be between 0 and {len(self._lists) - 1}"
            )

        # Remove from current position and insert at new position
        task_list = self._lists.pop(list_index)
        self._lists.insert(position, task_list)

        # Update custom indices for MANUAL strategy
        for i, tl in enumerate(self._lists):
            if tl.id in self._metadata:
                self._metadata[tl.id]["custom_index"] = i

        self._modified_at = datetime.now()

    def rename_list(self, list_id: int, new_name: str) -> None:
        """Rename a list.

        Args:
            list_id: ID of the list to rename
            new_name: New name for the list

        Raises:
            ValueError: If list_id doesn't exist
            ValueError: If new_name is invalid
        """
        task_list = self.get_list(list_id)
        if task_list is None:
            raise ValueError(f"List with ID {list_id} not found")

        task_list.name = new_name
        self._modified_at = datetime.now()

    def get_lists_with_metadata(
        self,
    ) -> List[Tuple[TaskList, dict]]:
        """Get all lists with their metadata.

        Returns:
            List of tuples (TaskList, metadata_dict) sorted by strategy
        """
        lists = self.get_lists()
        return [
            (task_list, self._metadata.get(task_list.id, {}))
            for task_list in lists
        ]

    def to_dict(self) -> dict:
        """Convert container to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the container and all lists
        """
        # Convert metadata datetimes to ISO format
        serialized_metadata = {}
        for list_id, meta in self._metadata.items():
            serialized_metadata[str(list_id)] = {
                "custom_index": meta["custom_index"],
                "created_at": (
                    meta["created_at"].isoformat()
                    if isinstance(meta["created_at"], datetime)
                    else meta["created_at"]
                ),
            }

        return {
            "ordering_strategy": self._ordering_strategy.value,
            "created_at": self._created_at.isoformat(),
            "modified_at": self._modified_at.isoformat(),
            "lists": [task_list.to_dict() for task_list in self._lists],
            "metadata": serialized_metadata,
        }

    def __repr__(self) -> str:
        """Return string representation of the container."""
        return (
            f"ListContainer(strategy={self._ordering_strategy.value}, "
            f"list_count={self.list_count})"
        )

    def __eq__(self, other: object) -> bool:
        """Check if two containers are equal based on content."""
        if not isinstance(other, ListContainer):
            return False
        return (
            self._ordering_strategy == other._ordering_strategy
            and len(self._lists) == len(other._lists)
        )
