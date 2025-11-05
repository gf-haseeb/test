"""Unit tests for ListContainer class."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from my_todo_lib.core.list_container import ListContainer
from my_todo_lib.core.task_list import TaskList
from my_todo_lib.core.task import Task
from my_todo_lib.core.constants import OrderingStrategy, TaskStatus, Priority


class TestListContainerCreation:
    """Test ListContainer object creation."""

    def test_create_container_with_default_strategy(self):
        """Test creating a container with default strategy."""
        container = ListContainer()
        assert container.ordering_strategy == OrderingStrategy.MANUAL
        assert container.list_count == 0

    def test_create_container_with_custom_strategy(self):
        """Test creating a container with custom strategy."""
        container = ListContainer(ordering_strategy=OrderingStrategy.ALPHABETICAL)
        assert container.ordering_strategy == OrderingStrategy.ALPHABETICAL

    def test_invalid_strategy_raises_error(self):
        """Test that invalid strategy raises ValueError."""
        with pytest.raises(ValueError, match="ordering_strategy must be"):
            ListContainer(ordering_strategy="invalid")


class TestListContainerListManagement:
    """Test adding and removing lists from container."""

    def test_create_list(self):
        """Test creating a list in the container."""
        container = ListContainer()
        task_list = container.create_list(name="Work")
        assert container.list_count == 1
        assert task_list.name == "Work"

    def test_create_multiple_lists(self):
        """Test creating multiple lists."""
        container = ListContainer()
        list1 = container.create_list("Work")
        list2 = container.create_list("Personal")
        list3 = container.create_list("Shopping")
        assert container.list_count == 3

    def test_add_existing_list(self):
        """Test adding an existing TaskList."""
        container = ListContainer()
        task_list = TaskList(name="Work")
        container.add_list(task_list)
        assert container.list_count == 1

    def test_add_same_list_twice_raises_error(self):
        """Test that adding the same list twice raises ValueError."""
        container = ListContainer()
        task_list = TaskList(name="Work")
        container.add_list(task_list)
        with pytest.raises(ValueError, match="already exists"):
            container.add_list(task_list)

    def test_add_non_list_object_raises_error(self):
        """Test that adding non-TaskList object raises TypeError."""
        container = ListContainer()
        with pytest.raises(TypeError, match="Expected TaskList instance"):
            container.add_list("Not a list")

    def test_remove_list_by_id(self):
        """Test removing a list by ID."""
        container = ListContainer()
        task_list = container.create_list("Work")
        result = container.remove_list(task_list.id)
        assert result is True
        assert container.list_count == 0

    def test_remove_nonexistent_list_returns_false(self):
        """Test that removing non-existent list returns False."""
        container = ListContainer()
        result = container.remove_list(999)
        assert result is False

    def test_get_list_by_id(self):
        """Test retrieving a list by ID."""
        container = ListContainer()
        task_list = container.create_list("Work")
        retrieved = container.get_list(task_list.id)
        assert retrieved == task_list
        assert retrieved.name == "Work"

    def test_get_nonexistent_list_returns_none(self):
        """Test that getting non-existent list returns None."""
        container = ListContainer()
        result = container.get_list(999)
        assert result is None


class TestListContainerOrdering:
    """Test list ordering strategies."""

    def test_manual_ordering(self):
        """Test manual ordering strategy."""
        container = ListContainer(ordering_strategy=OrderingStrategy.MANUAL)
        list1 = container.create_list("Work")
        list2 = container.create_list("Personal")
        list3 = container.create_list("Shopping")

        lists = container.get_lists()
        assert lists[0].name == "Work"
        assert lists[1].name == "Personal"
        assert lists[2].name == "Shopping"

    def test_alphabetical_ordering(self):
        """Test alphabetical ordering strategy."""
        container = ListContainer(
            ordering_strategy=OrderingStrategy.ALPHABETICAL
        )
        container.create_list("Work")
        container.create_list("Personal")
        container.create_list("Shopping")

        lists = container.get_lists()
        names = [l.name for l in lists]
        assert names == sorted(names)

    def test_creation_order_ordering(self):
        """Test creation order ordering strategy."""
        container = ListContainer(
            ordering_strategy=OrderingStrategy.CREATION_ORDER
        )
        list1 = container.create_list("First")
        list2 = container.create_list("Second")
        list3 = container.create_list("Third")

        lists = container.get_lists()
        assert lists[0].id == list1.id
        assert lists[1].id == list2.id
        assert lists[2].id == list3.id

    def test_recently_modified_ordering(self):
        """Test recently modified ordering strategy."""
        container = ListContainer(
            ordering_strategy=OrderingStrategy.RECENTLY_MODIFIED
        )
        list1 = container.create_list("Oldest")
        list2 = container.create_list("Newest")

        lists = container.get_lists()
        # Newest should be first (reverse chronological)
        assert lists[0].name == "Newest"
        assert lists[1].name == "Oldest"

    def test_recently_added_task_ordering(self):
        """Test recently added task ordering strategy."""
        container = ListContainer(
            ordering_strategy=OrderingStrategy.RECENTLY_ADDED_TASK
        )
        list1 = container.create_list("List1")
        list2 = container.create_list("List2")

        # Add task to list2
        task = Task(title="Test task")
        list2.add_task(task)

        lists = container.get_lists()
        # List2 should be first because it has the most recent task
        assert lists[0].id == list2.id


class TestListContainerMoving:
    """Test moving lists (manual strategy)."""

    def test_move_list_manual_strategy(self):
        """Test moving a list with MANUAL strategy."""
        container = ListContainer(ordering_strategy=OrderingStrategy.MANUAL)
        list1 = container.create_list("First")
        list2 = container.create_list("Second")
        list3 = container.create_list("Third")

        container.move_list(list1.id, 2)
        lists = container.get_lists()

        assert lists[0].id == list2.id
        assert lists[1].id == list3.id
        assert lists[2].id == list1.id

    def test_move_list_non_manual_strategy_raises_error(self):
        """Test that moving with non-MANUAL strategy raises ValueError."""
        container = ListContainer(
            ordering_strategy=OrderingStrategy.ALPHABETICAL
        )
        list1 = container.create_list("Work")
        with pytest.raises(ValueError, match="MANUAL ordering strategy"):
            container.move_list(list1.id, 0)

    def test_move_nonexistent_list_raises_error(self):
        """Test that moving non-existent list raises ValueError."""
        container = ListContainer(ordering_strategy=OrderingStrategy.MANUAL)
        with pytest.raises(ValueError, match="not found"):
            container.move_list(999, 0)

    def test_move_to_invalid_position_raises_error(self):
        """Test that moving to invalid position raises ValueError."""
        container = ListContainer(ordering_strategy=OrderingStrategy.MANUAL)
        list1 = container.create_list("Work")
        with pytest.raises(ValueError, match="Position must be between"):
            container.move_list(list1.id, 5)


class TestListContainerStrategyChange:
    """Test changing ordering strategies."""

    def test_change_ordering_strategy(self):
        """Test changing the ordering strategy."""
        container = ListContainer(ordering_strategy=OrderingStrategy.MANUAL)
        assert container.ordering_strategy == OrderingStrategy.MANUAL

        container.set_ordering_strategy(OrderingStrategy.ALPHABETICAL)
        assert container.ordering_strategy == OrderingStrategy.ALPHABETICAL

    def test_change_to_invalid_strategy_raises_error(self):
        """Test that changing to invalid strategy raises ValueError."""
        container = ListContainer()
        with pytest.raises(ValueError, match="strategy must be"):
            container.set_ordering_strategy("invalid")


class TestListContainerRenaming:
    """Test renaming lists."""

    def test_rename_list(self):
        """Test renaming a list."""
        container = ListContainer()
        task_list = container.create_list("Old Name")
        container.rename_list(task_list.id, "New Name")

        retrieved = container.get_list(task_list.id)
        assert retrieved.name == "New Name"

    def test_rename_nonexistent_list_raises_error(self):
        """Test that renaming non-existent list raises ValueError."""
        container = ListContainer()
        with pytest.raises(ValueError, match="not found"):
            container.rename_list(999, "New Name")


class TestListContainerRetrieval:
    """Test retrieving lists from container."""

    def test_get_all_lists(self):
        """Test getting all lists without ordering."""
        container = ListContainer(
            ordering_strategy=OrderingStrategy.ALPHABETICAL
        )
        list1 = container.create_list("Work")
        list2 = container.create_list("Personal")

        all_lists = container.get_all_lists()
        assert len(all_lists) == 2
        # Should be in creation order, not alphabetical
        assert all_lists[0].id == list1.id
        assert all_lists[1].id == list2.id

    def test_get_all_lists_returns_copy(self):
        """Test that get_all_lists returns a copy."""
        container = ListContainer()
        list1 = container.create_list("Work")
        lists = container.get_all_lists()
        lists.append(TaskList(name="New"))

        assert container.list_count == 1  # Original unchanged

    def test_get_lists_with_metadata(self):
        """Test getting lists with metadata."""
        container = ListContainer()
        list1 = container.create_list("Work")

        lists_with_meta = container.get_lists_with_metadata()
        assert len(lists_with_meta) == 1
        task_list, metadata = lists_with_meta[0]
        assert task_list.name == "Work"
        assert "custom_index" in metadata


class TestListContainerSerialization:
    """Test serialization of container."""

    def test_to_dict(self):
        """Test converting container to dictionary."""
        container = ListContainer(
            ordering_strategy=OrderingStrategy.RECENTLY_MODIFIED
        )
        list1 = container.create_list("Work")
        task = Task(title="Task 1")
        list1.add_task(task)

        container_dict = container.to_dict()

        assert container_dict["ordering_strategy"] == "recently_modified"
        assert len(container_dict["lists"]) == 1
        assert container_dict["lists"][0]["name"] == "Work"
        assert container_dict["lists"][0]["tasks"][0]["title"] == "Task 1"

    def test_to_dict_empty_container(self):
        """Test serializing empty container."""
        container = ListContainer()
        container_dict = container.to_dict()

        assert container_dict["ordering_strategy"] == "manual"
        assert container_dict["lists"] == []


class TestListContainerRepr:
    """Test string representation."""

    def test_repr(self):
        """Test __repr__ method."""
        container = ListContainer(ordering_strategy=OrderingStrategy.MANUAL)
        list1 = container.create_list("Work")

        repr_str = repr(container)
        assert "manual" in repr_str
        assert "1" in repr_str  # list_count


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
