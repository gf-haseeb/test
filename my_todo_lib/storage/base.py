"""Abstract base class for storage backends."""

from abc import ABC, abstractmethod
from my_todo_lib.core.list_container import ListContainer


class Storage(ABC):
    """Abstract base class for task storage implementations.

    All storage backends should inherit from this class and implement
    the abstract methods to provide persistence functionality.
    """

    @abstractmethod
    def save(self, container: ListContainer) -> None:
        """Save a ListContainer to persistent storage.

        Args:
            container: ListContainer object to save

        Raises:
            IOError: If save operation fails
        """
        pass

    @abstractmethod
    def load(self) -> ListContainer:
        """Load a ListContainer from persistent storage.

        Returns:
            Loaded ListContainer object, or empty container if not found

        Raises:
            IOError: If load operation fails
            ValueError: If stored data is invalid
        """
        pass

    @abstractmethod
    def exists(self) -> bool:
        """Check if storage contains saved data.

        Returns:
            True if data exists in storage, False otherwise
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all data from storage.

        Raises:
            IOError: If clear operation fails
        """
        pass
