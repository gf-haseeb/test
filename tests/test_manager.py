"""Unit tests for TaskManager."""

import sys
import os
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from my_todo_lib.manager import TaskManager
from my_todo_lib.core.task import Task
from my_todo_lib.core.constants import Priority, TaskStatus, OrderingStrategy
from my_todo_lib.storage.json_storage import JSONStorage


class TestTaskManagerListOperations:
    """Test TaskManager list management."""

    def test_create_list(self):
        """Test creating a list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            assert task_list.name == "Work"
            assert task_list.id is not None

    def test_get_lists(self):
        """Test getting all lists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            manager.create_list("Work")
            manager.create_list("Personal")

            lists = manager.get_lists()
            assert len(lists) == 2

    def test_get_list_by_id(self):
        """Test getting a specific list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            retrieved = manager.get_list(task_list.id)

            assert retrieved is not None
            assert retrieved.name == "Work"

    def test_delete_list(self):
        """Test deleting a list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            manager.delete_list(task_list.id)

            assert manager.get_list(task_list.id) is None

    def test_rename_list(self):
        """Test renaming a list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            manager.rename_list(task_list.id, "Job")

            updated = manager.get_list(task_list.id)
            assert updated.name == "Job"

    def test_set_list_ordering(self):
        """Test setting list ordering strategy."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            manager.set_list_ordering(OrderingStrategy.ALPHABETICAL)
            assert (
                manager.container.ordering_strategy
                == OrderingStrategy.ALPHABETICAL
            )

    def test_move_list(self):
        """Test moving list position."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            list1 = manager.create_list("First")
            list2 = manager.create_list("Second")
            list3 = manager.create_list("Third")

            manager.move_list(list1.id, 2)
            lists = manager.get_lists()
            assert lists[2].id == list1.id


class TestTaskManagerTaskOperations:
    """Test TaskManager task management."""

    def test_add_task_to_list(self):
        """Test adding a task to a list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            task = manager.add_task_to_list(task_list.id, "Fix bug")

            assert task.title == "Fix bug"
            assert task_list.task_count == 1

    def test_get_task(self):
        """Test retrieving a task."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            added_task = manager.add_task_to_list(
                task_list.id, "Fix bug", priority=Priority.HIGH
            )

            retrieved = manager.get_task(task_list.id, added_task.id)
            assert retrieved.title == "Fix bug"
            assert retrieved.priority == Priority.HIGH

    def test_get_tasks_from_list(self):
        """Test getting all tasks from a list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            manager.add_task_to_list(task_list.id, "Task 1")
            manager.add_task_to_list(task_list.id, "Task 2")

            tasks = manager.get_tasks(task_list.id)
            assert len(tasks) == 2

    def test_update_task_status(self):
        """Test updating task status."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            task = manager.add_task_to_list(task_list.id, "Fix bug")

            manager.update_task(
                task_list.id, task.id, status=TaskStatus.IN_PROGRESS
            )

            updated = manager.get_task(task_list.id, task.id)
            assert updated.status == TaskStatus.IN_PROGRESS

    def test_update_task_priority(self):
        """Test updating task priority."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            task = manager.add_task_to_list(task_list.id, "Fix bug")

            manager.update_task(task_list.id, task.id, priority=Priority.HIGH)

            updated = manager.get_task(task_list.id, task.id)
            assert updated.priority == Priority.HIGH

    def test_delete_task(self):
        """Test deleting a task."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            task = manager.add_task_to_list(task_list.id, "Fix bug")

            manager.delete_task(task_list.id, task.id)

            assert manager.get_task(task_list.id, task.id) is None

    def test_move_task_to_list(self):
        """Test moving a task to another list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            # Create two lists
            list1 = manager.create_list("Work")
            list2 = manager.create_list("Personal")

            # Add task to list1
            task = manager.add_task_to_list(list1.id, "Fix bug")
            assert manager.get_task(list1.id, task.id) is not None

            # Move task to list2
            moved_task = manager.move_task_to_list(list1.id, task.id, list2.id)

            # Verify task is no longer in list1
            assert manager.get_task(list1.id, task.id) is None

            # Verify task is now in list2
            assert manager.get_task(list2.id, task.id) is not None
            assert moved_task.title == "Fix bug"

    def test_move_task_to_list_same_list_error(self):
        """Test moving task to same list raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            list1 = manager.create_list("Work")
            task = manager.add_task_to_list(list1.id, "Fix bug")

            # Try to move to same list
            with pytest.raises(ValueError, match="Source and target lists cannot be the same"):
                manager.move_task_to_list(list1.id, task.id, list1.id)

    def test_move_task_source_list_not_found(self):
        """Test moving task from non-existent source list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            list1 = manager.create_list("Work")

            with pytest.raises(ValueError, match="Source list with ID"):
                manager.move_task_to_list(999, 1, list1.id)

    def test_move_task_target_list_not_found(self):
        """Test moving task to non-existent target list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            list1 = manager.create_list("Work")
            task = manager.add_task_to_list(list1.id, "Fix bug")

            with pytest.raises(ValueError, match="Target list with ID"):
                manager.move_task_to_list(list1.id, task.id, 999)

    def test_move_task_not_found(self):
        """Test moving non-existent task."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            list1 = manager.create_list("Work")
            list2 = manager.create_list("Personal")

            with pytest.raises(ValueError, match="Task with ID"):
                manager.move_task_to_list(list1.id, 999, list2.id)

    def test_move_task_preserves_data(self):
        """Test that moving task preserves all its data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            list1 = manager.create_list("Work")
            list2 = manager.create_list("Personal")

            # Create task with all properties
            task = manager.add_task_to_list(
                list1.id,
                title="Important task",
                description="This is important",
                priority=Priority.HIGH,
                status=TaskStatus.IN_PROGRESS,
                tags=["urgent", "work"]
            )

            # Move task to list2
            moved_task = manager.move_task_to_list(list1.id, task.id, list2.id)

            # Verify all properties are preserved
            assert moved_task.title == "Important task"
            assert moved_task.description == "This is important"
            assert moved_task.priority == Priority.HIGH
            assert moved_task.status == TaskStatus.IN_PROGRESS
            assert moved_task.tags == ["urgent", "work"]


class TestTaskManagerSearch:
    """Test TaskManager search functionality."""

    def test_search_tasks_by_title(self):
        """Test searching tasks by title."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            list1 = manager.create_list("Work")
            list2 = manager.create_list("Personal")

            manager.add_task_to_list(list1.id, "Fix database bug")
            manager.add_task_to_list(list1.id, "Review PR")
            manager.add_task_to_list(list2.id, "Buy groceries")

            results = manager.search_tasks_across_lists("bug")
            assert len(results) == 1
            task_list, task = results[0]
            assert task.title == "Fix database bug"

    def test_search_tasks_by_description(self):
        """Test searching tasks by description."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            manager.add_task_to_list(
                task_list.id, "Task", description="Fix urgent database issue"
            )

            results = manager.search_tasks_across_lists("database", search_in="description")
            assert len(results) == 1

    def test_search_tasks_by_tags(self):
        """Test searching tasks by tags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            task = Task(title="Urgent task", tags=["urgent", "critical"])
            task_list.add_task(task)

            results = manager.search_tasks_across_lists("urgent", search_in="tags")
            assert len(results) == 1

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            manager.add_task_to_list(task_list.id, "FIX BUG")

            results = manager.search_tasks_across_lists("fix")
            assert len(results) == 1


class TestTaskManagerPersistence:
    """Test TaskManager persistence and auto-save."""

    def test_save_persists_data(self):
        """Test that save persists data to storage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)
            manager = TaskManager(storage=storage)

            task_list = manager.create_list("Work")
            manager.add_task_to_list(task_list.id, "Fix bug")

            manager.save()

            # Create new manager and verify data persists
            manager2 = TaskManager(storage=JSONStorage(file_path))
            manager2.load()

            lists = manager2.get_lists()
            assert len(lists) == 1
            assert lists[0].name == "Work"

    def test_load_restores_data(self):
        """Test that load restores data from storage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)

            # Create and save
            manager1 = TaskManager(storage=storage)
            list1 = manager1.create_list("Work")
            task1 = manager1.add_task_to_list(list1.id, "Task 1")
            manager1.save()

            # Load in new manager
            manager2 = TaskManager(storage=JSONStorage(file_path))
            manager2.load()

            loaded_lists = manager2.get_lists()
            assert len(loaded_lists) == 1
            assert loaded_lists[0].task_count == 1

    def test_clear_deletes_all_data(self):
        """Test that clear removes all data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            manager.create_list("Work")
            manager.save()

            manager.clear()

            # New manager should have no data
            manager2 = TaskManager(storage=JSONStorage(file_path))
            assert manager2.get_lists() == []


class TestTaskManagerStatistics:
    """Test TaskManager statistics."""

    def test_get_statistics(self):
        """Test getting statistics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            manager.add_task_to_list(task_list.id, "Task 1")
            manager.add_task_to_list(task_list.id, "Task 2")

            stats = manager.get_statistics()
            assert stats["total_tasks"] == 2
            assert stats["total_lists"] == 1
            assert stats["todo_tasks"] == 2

    def test_statistics_with_completed_tasks(self):
        """Test statistics with completed tasks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            task1 = manager.add_task_to_list(task_list.id, "Task 1")
            manager.add_task_to_list(task_list.id, "Task 2")

            manager.update_task(
                task_list.id, task1.id, status=TaskStatus.COMPLETED
            )

            stats = manager.get_statistics()
            assert stats["completed_tasks"] == 1
            assert stats["todo_tasks"] == 1


class TestTaskManagerAutoSave:
    """Test TaskManager auto-save on mutations."""

    def test_auto_save_on_create_list(self):
        """Test that create_list triggers auto-save."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)
            manager = TaskManager(storage=storage)

            manager.create_list("Work")

            # Verify file was created
            assert storage.exists()

    def test_auto_save_on_add_task(self):
        """Test that add_task_to_list triggers auto-save."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            manager.add_task_to_list(task_list.id, "Fix bug")

            # Verify data persists
            manager2 = TaskManager(storage=JSONStorage(file_path))
            manager2.load()
            assert manager2.get_lists()[0].task_count == 1

    def test_auto_save_on_update_task(self):
        """Test that update_task triggers auto-save."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            task = manager.add_task_to_list(task_list.id, "Fix bug")

            manager.update_task(
                task_list.id, task.id, status=TaskStatus.COMPLETED
            )

            # Verify status persists
            manager2 = TaskManager(storage=JSONStorage(file_path))
            manager2.load()
            loaded_task = manager2.get_task(task_list.id, task.id)
            assert loaded_task.status == TaskStatus.COMPLETED


class TestTaskManagerErrorHandling:
    """Test TaskManager error handling."""

    def test_add_task_to_nonexistent_list(self):
        """Test adding task to non-existent list raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            with pytest.raises(ValueError):
                manager.add_task_to_list(999, "Task")

    def test_get_nonexistent_task(self):
        """Test getting non-existent task returns None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            task_list = manager.create_list("Work")
            task = manager.get_task(task_list.id, 999)

            assert task is None

    def test_delete_nonexistent_list(self):
        """Test deleting non-existent list raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            manager = TaskManager(storage=JSONStorage(file_path))

            with pytest.raises(ValueError):
                manager.delete_list(999)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
