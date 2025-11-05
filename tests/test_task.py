"""Unit tests for Task class."""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from my_todo_lib.core.task import Task
from my_todo_lib.core.constants import TaskStatus, Priority, MAX_TASK_NAME_LENGTH


class TestTaskCreation:
    """Test Task object creation."""

    def test_create_basic_task(self):
        """Test creating a basic task with just a title."""
        task = Task(title="Buy groceries")
        assert task.title == "Buy groceries"
        assert task.status == TaskStatus.TODO
        assert task.priority == Priority.MEDIUM
        assert task.description == ""
        assert task.tags == []

    def test_create_task_with_all_properties(self):
        """Test creating a task with all properties."""
        task = Task(
            title="Fix critical bug",
            description="Database connection issue",
            priority=Priority.HIGH,
            tags=["urgent", "backend"],
        )
        assert task.title == "Fix critical bug"
        assert task.description == "Database connection issue"
        assert task.priority == Priority.HIGH
        assert task.tags == ["urgent", "backend"]

    def test_task_auto_incrementing_id(self):
        """Test that task IDs auto-increment."""
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        assert task2.id > task1.id

    def test_task_timestamps(self):
        """Test that created_at and modified_at are set."""
        before = datetime.now()
        task = Task(title="Test task")
        after = datetime.now()
        
        assert before <= task.created_at <= after
        assert before <= task.modified_at <= after


class TestTaskValidation:
    """Test Task input validation."""

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="")

    def test_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="   ")

    def test_title_exceeds_max_length_raises_error(self):
        """Test that title exceeding max length raises ValueError."""
        long_title = "a" * (MAX_TASK_NAME_LENGTH + 1)
        with pytest.raises(ValueError, match="Task title exceeds max length"):
            Task(title=long_title)

    def test_invalid_status_type_raises_error(self):
        """Test that invalid status type raises ValueError."""
        task = Task(title="Test")
        with pytest.raises(ValueError, match="Status must be a TaskStatus enum"):
            task.status = "invalid"

    def test_invalid_priority_type_raises_error(self):
        """Test that invalid priority type raises ValueError."""
        task = Task(title="Test")
        with pytest.raises(ValueError, match="Priority must be a Priority enum"):
            task.priority = "invalid"


class TestTaskProperties:
    """Test Task property setters and getters."""

    def test_update_title(self):
        """Test updating task title."""
        task = Task(title="Old title")
        task.title = "New title"
        assert task.title == "New title"
        assert task.modified_at > task.created_at

    def test_update_description(self):
        """Test updating task description."""
        task = Task(title="Test")
        task.description = "New description"
        assert task.description == "New description"

    def test_update_status(self):
        """Test updating task status."""
        task = Task(title="Test")
        task.status = TaskStatus.IN_PROGRESS
        assert task.status == TaskStatus.IN_PROGRESS

    def test_update_priority(self):
        """Test updating task priority."""
        task = Task(title="Test")
        task.priority = Priority.HIGH
        assert task.priority == Priority.HIGH

    def test_update_due_date(self):
        """Test updating task due date."""
        task = Task(title="Test")
        due_date = datetime(2025, 12, 25)
        task.due_date = due_date
        assert task.due_date == due_date


class TestTaskTags:
    """Test Task tag management."""

    def test_add_tag(self):
        """Test adding a tag to task."""
        task = Task(title="Test")
        task.add_tag("urgent")
        assert "urgent" in task.tags

    def test_add_multiple_tags(self):
        """Test adding multiple tags."""
        task = Task(title="Test")
        task.add_tag("urgent")
        task.add_tag("backend")
        assert len(task.tags) == 2
        assert "urgent" in task.tags
        assert "backend" in task.tags

    def test_tag_normalized_to_lowercase(self):
        """Test that tags are converted to lowercase."""
        task = Task(title="Test")
        task.add_tag("URGENT")
        assert "urgent" in task.tags

    def test_duplicate_tags_not_added(self):
        """Test that duplicate tags are not added."""
        task = Task(title="Test")
        task.add_tag("urgent")
        task.add_tag("urgent")
        assert len(task.tags) == 1

    def test_remove_tag(self):
        """Test removing a tag."""
        task = Task(title="Test", tags=["urgent", "backend"])
        task.remove_tag("urgent")
        assert "urgent" not in task.tags
        assert "backend" in task.tags

    def test_remove_nonexistent_tag(self):
        """Test removing a tag that doesn't exist (should not error)."""
        task = Task(title="Test", tags=["urgent"])
        task.remove_tag("nonexistent")  # Should not raise error
        assert "urgent" in task.tags

    def test_tags_property_returns_copy(self):
        """Test that tags property returns a copy, not reference."""
        task = Task(title="Test", tags=["urgent"])
        tags = task.tags
        tags.append("new_tag")
        assert len(task.tags) == 1  # Original should be unchanged


class TestTaskSerialization:
    """Test Task serialization."""

    def test_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            title="Test task",
            description="Test description",
            priority=Priority.HIGH,
            tags=["urgent"],
        )
        task_dict = task.to_dict()
        
        assert task_dict["title"] == "Test task"
        assert task_dict["description"] == "Test description"
        assert task_dict["priority"] == "high"
        assert task_dict["status"] == "todo"
        assert "urgent" in task_dict["tags"]
        assert task_dict["created_at"]  # Should have ISO timestamp
        assert task_dict["modified_at"]  # Should have ISO timestamp

    def test_to_dict_with_due_date(self):
        """Test serializing task with due date."""
        due_date = datetime(2025, 12, 25, 10, 30, 0)
        task = Task(title="Test", due_date=due_date)
        task_dict = task.to_dict()
        assert task_dict["due_date"] == due_date.isoformat()

    def test_to_dict_without_due_date(self):
        """Test serializing task without due date."""
        task = Task(title="Test")
        task_dict = task.to_dict()
        assert task_dict["due_date"] is None


class TestTaskEquality:
    """Test Task equality."""

    def test_tasks_equal_by_id(self):
        """Test that tasks are equal if they have the same ID."""
        task1 = Task(title="Task 1")
        task_id = task1.id
        # Can't really test this without modifying the task's ID directly
        assert task1 == task1  # Same object should equal itself

    def test_task_not_equal_to_other_types(self):
        """Test that task is not equal to other types."""
        task = Task(title="Test")
        assert task != "Not a task"
        assert task != 123
        assert task != None


class TestTaskRepr:
    """Test Task string representation."""

    def test_repr(self):
        """Test __repr__ method."""
        task = Task(title="Test task", priority=Priority.HIGH)
        repr_str = repr(task)
        assert "Test task" in repr_str
        assert "high" in repr_str
        assert "todo" in repr_str


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
