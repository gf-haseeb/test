"""JSON file-based storage implementation."""

import json
import os
from datetime import datetime
from typing import Dict, Any
from my_todo_lib.storage.base import Storage
from my_todo_lib.core.list_container import ListContainer
from my_todo_lib.core.task_list import TaskList
from my_todo_lib.core.task import Task
from my_todo_lib.core.constants import TaskStatus, Priority, OrderingStrategy


class JSONStorage(Storage):
    """Stores task data in JSON files for persistence.

    Attributes:
        file_path: Path to the JSON file for storage
    """

    def __init__(self, file_path: str = "tasks.json"):
        """Initialize JSONStorage with file path.

        Args:
            file_path: Path where JSON data will be stored (default: tasks.json)
        """
        self._file_path = file_path

    @property
    def file_path(self) -> str:
        """Get the storage file path."""
        return self._file_path

    def save(self, container: ListContainer) -> None:
        """Save ListContainer to JSON file.

        Args:
            container: ListContainer to save

        Raises:
            IOError: If file write fails
        """
        try:
            data = container.to_dict()
            with open(self._file_path, "w") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to save to {self._file_path}: {str(e)}")
        except Exception as e:
            raise IOError(f"Unexpected error saving to JSON: {str(e)}")

    def load(self) -> ListContainer:
        """Load ListContainer from JSON file.

        Returns:
            Loaded ListContainer, or empty container if file doesn't exist

        Raises:
            ValueError: If JSON data is invalid or corrupted
            IOError: If file read fails
        """
        if not self.exists():
            # Return empty container if file doesn't exist
            return ListContainer()

        try:
            with open(self._file_path, "r") as f:
                data = json.load(f)

            # Reconstruct ListContainer from dictionary
            return self._dict_to_container(data)

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self._file_path}: {str(e)}")
        except IOError as e:
            raise IOError(f"Failed to read from {self._file_path}: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error loading data from JSON: {str(e)}")

    def exists(self) -> bool:
        """Check if storage file exists.

        Returns:
            True if file exists, False otherwise
        """
        return os.path.exists(self._file_path)

    def clear(self) -> None:
        """Delete the storage file.

        Raises:
            IOError: If file deletion fails
        """
        try:
            if self.exists():
                os.remove(self._file_path)
        except IOError as e:
            raise IOError(f"Failed to clear storage file: {str(e)}")

    def _dict_to_container(self, data: Dict[str, Any]) -> ListContainer:
        """Convert dictionary to ListContainer.

        Args:
            data: Dictionary representation from JSON

        Returns:
            Reconstructed ListContainer object

        Raises:
            ValueError: If data structure is invalid
        """
        try:
            # Get ordering strategy
            strategy_str = data.get("ordering_strategy", "manual")
            ordering_strategy = OrderingStrategy[strategy_str.upper()]

            # Create container
            container = ListContainer(ordering_strategy=ordering_strategy)

            # Restore lists and tasks
            for list_data in data.get("lists", []):
                task_list = self._dict_to_task_list(list_data)
                container.add_list(task_list)

            # Restore metadata with datetime conversion
            if "metadata" in data:
                for list_id_str, meta in data["metadata"].items():
                    # Convert list_id back to int
                    list_id = int(list_id_str)
                    container._metadata[list_id] = {
                        "custom_index": meta["custom_index"],
                        "created_at": (
                            datetime.fromisoformat(meta["created_at"])
                            if isinstance(meta["created_at"], str)
                            else meta["created_at"]
                        ),
                    }

            return container

        except KeyError as e:
            raise ValueError(f"Missing required field in JSON: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error reconstructing container: {str(e)}")

    def _dict_to_task_list(self, data: Dict[str, Any]) -> TaskList:
        """Convert dictionary to TaskList.

        Args:
            data: Dictionary representation of task list

        Returns:
            Reconstructed TaskList object

        Raises:
            ValueError: If data structure is invalid
        """
        try:
            # Restore with original ID
            task_list = TaskList(
                name=data["name"],
                description=data["description"],
                id_=data.get("id"),
            )

            # Restore tasks
            for task_data in data.get("tasks", []):
                task = self._dict_to_task(task_data)
                task_list.add_task(task)

            return task_list

        except KeyError as e:
            raise ValueError(f"Missing required field in task list: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error reconstructing task list: {str(e)}")

    def _dict_to_task(self, data: Dict[str, Any]) -> Task:
        """Convert dictionary to Task.

        Args:
            data: Dictionary representation of task

        Returns:
            Reconstructed Task object

        Raises:
            ValueError: If data structure is invalid
        """
        try:
            # Parse status and priority
            status = TaskStatus[data["status"].upper()]
            priority = Priority[data["priority"].upper()]

            # Parse due date if present
            due_date = None
            if data.get("due_date"):
                due_date = datetime.fromisoformat(data["due_date"])

            # Create task with original ID
            task = Task(
                title=data["title"],
                description=data["description"],
                status=status,
                priority=priority,
                due_date=due_date,
                tags=data.get("tags", []),
                id_=data.get("id"),
            )

            return task

        except KeyError as e:
            raise ValueError(f"Missing required field in task: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error reconstructing task: {str(e)}")
