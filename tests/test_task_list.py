"""Unit tests for TaskList class."""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from my_todo_lib.core.task_list import TaskList
from my_todo_lib.core.task import Task
from my_todo_lib.core.constants import TaskStatus, Priority, MAX_LIST_NAME_LENGTH


class TestTaskListCreation:
    """Test TaskList object creation."""

    def test_create_basic_list(self):
        """Test creating a basic task list."""
        task_list = TaskList(name="Work Tasks")
        assert task_list.name == "Work Tasks"
        assert task_list.description == ""
        assert task_list.task_count == 0

    def test_create_list_with_description(self):
        """Test creating a list with description."""
        task_list = TaskList(name="Work", description="All work tasks")
        assert task_list.name == "Work"
        assert task_list.description == "All work tasks"

    def test_list_auto_incrementing_id(self):
        """Test that list IDs auto-increment."""
        list1 = TaskList(name="List 1")
        list2 = TaskList(name="List 2")
        assert list2.id > list1.id

    def test_list_timestamps(self):
        """Test that created_at and modified_at are set."""
        before = datetime.now()
        task_list = TaskList(name="Test list")
        after = datetime.now()
        
        assert before <= task_list.created_at <= after
        assert before <= task_list.modified_at <= after


class TestTaskListValidation:
    """Test TaskList input validation."""

    def test_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="List name cannot be empty"):
            TaskList(name="")

    def test_whitespace_only_name_raises_error(self):
        """Test that whitespace-only name raises ValueError."""
        with pytest.raises(ValueError, match="List name cannot be empty"):
            TaskList(name="   ")

    def test_name_exceeds_max_length_raises_error(self):
        """Test that name exceeding max length raises ValueError."""
        long_name = "a" * (MAX_LIST_NAME_LENGTH + 1)
        with pytest.raises(ValueError, match="List name exceeds max length"):
            TaskList(name=long_name)


class TestTaskListProperties:
    """Test TaskList property setters and getters."""

    def test_update_name(self):
        """Test updating list name."""
        task_list = TaskList(name="Old name")
        task_list.name = "New name"
        assert task_list.name == "New name"

    def test_update_description(self):
        """Test updating list description."""
        task_list = TaskList(name="Test")
        task_list.description = "New description"
        assert task_list.description == "New description"

    def test_update_name_strips_whitespace(self):
        """Test that name updates strip whitespace."""
        task_list = TaskList(name="Test")
        task_list.name = "  New name  "
        assert task_list.name == "New name"


class TestTaskListTaskManagement:
    """Test adding and removing tasks from list."""

    def test_add_task(self):
        """Test adding a task to list."""
        task_list = TaskList(name="Test")
        task = Task(title="Test task")
        task_list.add_task(task)
        assert task_list.task_count == 1

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks."""
        task_list = TaskList(name="Test")
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        task3 = Task(title="Task 3")
        
        task_list.add_task(task1)
        task_list.add_task(task2)
        task_list.add_task(task3)
        
        assert task_list.task_count == 3

    def test_add_same_task_twice_raises_error(self):
        """Test that adding the same task twice raises ValueError."""
        task_list = TaskList(name="Test")
        task = Task(title="Test task")
        task_list.add_task(task)
        
        with pytest.raises(ValueError, match="already exists in this list"):
            task_list.add_task(task)

    def test_add_non_task_object_raises_error(self):
        """Test that adding non-Task object raises TypeError."""
        task_list = TaskList(name="Test")
        with pytest.raises(TypeError, match="Expected Task instance"):
            task_list.add_task("Not a task")

    def test_remove_task_by_id(self):
        """Test removing a task by ID."""
        task_list = TaskList(name="Test")
        task = Task(title="Test task")
        task_list.add_task(task)
        
        result = task_list.remove_task(task.id)
        assert result is True
        assert task_list.task_count == 0

    def test_remove_nonexistent_task_returns_false(self):
        """Test that removing non-existent task returns False."""
        task_list = TaskList(name="Test")
        result = task_list.remove_task(999)
        assert result is False

    def test_get_task_by_id(self):
        """Test retrieving a task by ID."""
        task_list = TaskList(name="Test")
        task = Task(title="Test task")
        task_list.add_task(task)
        
        retrieved = task_list.get_task(task.id)
        assert retrieved == task
        assert retrieved.title == "Test task"

    def test_get_nonexistent_task_returns_none(self):
        """Test that getting non-existent task returns None."""
        task_list = TaskList(name="Test")
        result = task_list.get_task(999)
        assert result is None

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        task_list = TaskList(name="Test")
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        task_list.add_task(task1)
        task_list.add_task(task2)
        
        all_tasks = task_list.get_all_tasks()
        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task2 in all_tasks

    def test_get_all_tasks_returns_copy(self):
        """Test that get_all_tasks returns a copy, not reference."""
        task_list = TaskList(name="Test")
        task = Task(title="Test")
        task_list.add_task(task)
        
        tasks = task_list.get_all_tasks()
        tasks.append(Task(title="New"))
        
        assert task_list.task_count == 1  # Original should be unchanged


class TestTaskListFiltering:
    """Test filtering tasks in list."""

    def test_filter_tasks_by_status(self):
        """Test filtering tasks by status."""
        task_list = TaskList(name="Test")
        task1 = Task(title="Task 1", status=TaskStatus.TODO)
        task2 = Task(title="Task 2", status=TaskStatus.IN_PROGRESS)
        task3 = Task(title="Task 3", status=TaskStatus.TODO)
        
        task_list.add_task(task1)
        task_list.add_task(task2)
        task_list.add_task(task3)
        
        todo_tasks = task_list.get_tasks(status=TaskStatus.TODO)
        assert len(todo_tasks) == 2

    def test_filter_by_status_returns_empty_list(self):
        """Test filtering for status with no matching tasks."""
        task_list = TaskList(name="Test")
        task = Task(title="Task", status=TaskStatus.TODO)
        task_list.add_task(task)
        
        completed = task_list.get_tasks(status=TaskStatus.COMPLETED)
        assert len(completed) == 0

    def test_invalid_status_type_raises_error(self):
        """Test that invalid status type raises ValueError."""
        task_list = TaskList(name="Test")
        with pytest.raises(ValueError, match="Status must be TaskStatus enum"):
            task_list.get_tasks(status="invalid")


class TestTaskListSorting:
    """Test sorting tasks in list."""

    def test_sort_by_created_at(self):
        """Test sorting tasks by creation time."""
        task_list = TaskList(name="Test")
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        task_list.add_task(task1)
        task_list.add_task(task2)
        
        sorted_tasks = task_list.get_tasks(sort_by="created_at")
        assert sorted_tasks[0].id == task1.id
        assert sorted_tasks[1].id == task2.id

    def test_sort_by_priority(self):
        """Test sorting tasks by priority."""
        task_list = TaskList(name="Test")
        task1 = Task(title="Low", priority=Priority.LOW)
        task2 = Task(title="High", priority=Priority.HIGH)
        task3 = Task(title="Medium", priority=Priority.MEDIUM)
        
        task_list.add_task(task1)
        task_list.add_task(task2)
        task_list.add_task(task3)
        
        sorted_tasks = task_list.get_tasks(sort_by="priority")
        assert sorted_tasks[0].priority == Priority.HIGH
        assert sorted_tasks[1].priority == Priority.MEDIUM
        assert sorted_tasks[2].priority == Priority.LOW

    def test_invalid_sort_field_raises_error(self):
        """Test that invalid sort field raises ValueError."""
        task_list = TaskList(name="Test")
        with pytest.raises(ValueError, match="sort_by must be one of"):
            task_list.get_tasks(sort_by="invalid_field")


class TestTaskListCleanup:
    """Test task list cleanup operations."""

    def test_clear_completed_tasks(self):
        """Test clearing completed tasks."""
        task_list = TaskList(name="Test")
        task1 = Task(title="Task 1", status=TaskStatus.TODO)
        task2 = Task(title="Task 2", status=TaskStatus.COMPLETED)
        task3 = Task(title="Task 3", status=TaskStatus.IN_PROGRESS)
        
        task_list.add_task(task1)
        task_list.add_task(task2)
        task_list.add_task(task3)
        
        removed = task_list.clear_completed_tasks()
        assert removed == 1
        assert task_list.task_count == 2
        assert task_list.get_task(task2.id) is None

    def test_clear_completed_tasks_when_none_returns_zero(self):
        """Test clearing when no completed tasks."""
        task_list = TaskList(name="Test")
        task = Task(title="Task", status=TaskStatus.TODO)
        task_list.add_task(task)
        
        removed = task_list.clear_completed_tasks()
        assert removed == 0
        assert task_list.task_count == 1


class TestTaskListSerialization:
    """Test TaskList serialization."""

    def test_to_dict(self):
        """Test converting task list to dictionary."""
        task_list = TaskList(name="Work", description="Work tasks")
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        task_list.add_task(task1)
        task_list.add_task(task2)
        
        list_dict = task_list.to_dict()
        
        assert list_dict["name"] == "Work"
        assert list_dict["description"] == "Work tasks"
        assert len(list_dict["tasks"]) == 2
        assert list_dict["created_at"]
        assert list_dict["modified_at"]

    def test_to_dict_empty_list(self):
        """Test serializing empty task list."""
        task_list = TaskList(name="Empty")
        list_dict = task_list.to_dict()
        
        assert list_dict["name"] == "Empty"
        assert list_dict["tasks"] == []


class TestTaskListEquality:
    """Test TaskList equality."""

    def test_lists_equal_by_id(self):
        """Test that lists are equal if they have the same ID."""
        list1 = TaskList(name="List 1")
        assert list1 == list1  # Same object should equal itself

    def test_list_not_equal_to_other_types(self):
        """Test that list is not equal to other types."""
        task_list = TaskList(name="Test")
        assert task_list != "Not a list"
        assert task_list != 123


class TestTaskListRepr:
    """Test TaskList string representation."""

    def test_repr(self):
        """Test __repr__ method."""
        task_list = TaskList(name="Test list")
        task = Task(title="Task")
        task_list.add_task(task)
        
        repr_str = repr(task_list)
        assert "Test list" in repr_str
        assert "1" in repr_str  # task_count


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
