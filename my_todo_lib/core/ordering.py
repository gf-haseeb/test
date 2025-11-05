"""Ordering strategies for managing multiple lists."""

from typing import List, Callable
from datetime import datetime
from my_todo_lib.core.constants import OrderingStrategy


class OrderingStrategies:
    """Collection of ordering strategy implementations."""

    @staticmethod
    def manual(
        lists: List, metadata: dict
    ) -> List:
        """Return lists in manual order (custom_index).

        Args:
            lists: List of TaskList objects
            metadata: Dictionary with list metadata including custom_index

        Returns:
            Lists sorted by custom_index
        """
        def get_index(task_list):
            list_id = task_list.id
            if list_id in metadata:
                return metadata[list_id].get("custom_index", list_id)
            return list_id

        return sorted(lists, key=get_index)

    @staticmethod
    def recently_modified(
        lists: List, metadata: dict
    ) -> List:
        """Return lists sorted by modification time (newest first).

        Args:
            lists: List of TaskList objects
            metadata: Dictionary with list metadata

        Returns:
            Lists sorted by modified_at (descending)
        """
        return sorted(lists, key=lambda task_list: task_list.modified_at, reverse=True)

    @staticmethod
    def alphabetical(
        lists: List, metadata: dict
    ) -> List:
        """Return lists sorted alphabetically by name.

        Args:
            lists: List of TaskList objects
            metadata: Dictionary with list metadata

        Returns:
            Lists sorted alphabetically by name
        """
        return sorted(lists, key=lambda task_list: task_list.name.lower())

    @staticmethod
    def creation_order(
        lists: List, metadata: dict
    ) -> List:
        """Return lists sorted by creation time (oldest first).

        Args:
            lists: List of TaskList objects
            metadata: Dictionary with list metadata

        Returns:
            Lists sorted by created_at (ascending)
        """
        return sorted(lists, key=lambda task_list: task_list.created_at)

    @staticmethod
    def recently_added_task(
        lists: List, metadata: dict
    ) -> List:
        """Return lists sorted by most recent task (newest first).

        Args:
            lists: List of TaskList objects
            metadata: Dictionary with list metadata

        Returns:
            Lists sorted by most recent task modification time
        """
        def get_latest_task_time(task_list):
            if task_list.task_count == 0:
                return datetime.min

            all_tasks = task_list.get_all_tasks()
            if not all_tasks:
                return datetime.min

            return max(task.modified_at for task in all_tasks)

        return sorted(lists, key=get_latest_task_time, reverse=True)

    @staticmethod
    def get_strategy(
        strategy_enum: "OrderingStrategy",
    ) -> Callable:
        """Get the ordering function for a strategy.

        Args:
            strategy_enum: OrderingStrategy enum value

        Returns:
            Callable ordering function

        Raises:
            ValueError: If strategy is not recognized
        """
        strategies = {
            OrderingStrategy.MANUAL: OrderingStrategies.manual,
            OrderingStrategy.RECENTLY_MODIFIED: OrderingStrategies.recently_modified,
            OrderingStrategy.ALPHABETICAL: OrderingStrategies.alphabetical,
            OrderingStrategy.CREATION_ORDER: OrderingStrategies.creation_order,
            OrderingStrategy.RECENTLY_ADDED_TASK: OrderingStrategies.recently_added_task,
        }

        if strategy_enum not in strategies:
            raise ValueError(f"Unknown ordering strategy: {strategy_enum}")

        return strategies[strategy_enum]
