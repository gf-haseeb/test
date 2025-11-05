"""Unit tests for Storage implementations."""

import sys
import os
import tempfile
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from my_todo_lib.storage.json_storage import JSONStorage
from my_todo_lib.core.list_container import ListContainer
from my_todo_lib.core.task import Task
from my_todo_lib.core.constants import Priority, TaskStatus, OrderingStrategy


class TestJSONStorageBasics:
    """Test basic JSON storage operations."""

    def test_create_storage_with_default_path(self):
        """Test creating storage with default path."""
        storage = JSONStorage()
        assert storage.file_path == "tasks.json"

    def test_create_storage_with_custom_path(self):
        """Test creating storage with custom path."""
        storage = JSONStorage("/tmp/my_tasks.json")
        assert storage.file_path == "/tmp/my_tasks.json"

    def test_storage_file_does_not_exist_initially(self):
        """Test that storage file doesn't exist initially."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)
            assert storage.exists() is False

    def test_load_empty_storage_returns_empty_container(self):
        """Test loading from non-existent file returns empty container."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)
            container = storage.load()
            assert container.list_count == 0


class TestJSONStorageSaveLoad:
    """Test saving and loading data."""

    def test_save_empty_container(self):
        """Test saving an empty container."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)
            container = ListContainer()

            storage.save(container)
            assert storage.exists() is True

    def test_save_and_load_container_with_lists(self):
        """Test saving and loading container with lists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)

            # Create and save
            container = ListContainer()
            list1 = container.create_list("Work")
            list2 = container.create_list("Personal")
            storage.save(container)

            # Load and verify
            loaded = storage.load()
            assert loaded.list_count == 2
            assert loaded.get_list(list1.id).name == "Work"
            assert loaded.get_list(list2.id).name == "Personal"

    def test_save_and_load_container_with_tasks(self):
        """Test saving and loading container with tasks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)

            # Create and save
            container = ListContainer()
            task_list = container.create_list("Work")
            task1 = Task(title="Fix bug", priority=Priority.HIGH)
            task2 = Task(title="Review PR", priority=Priority.MEDIUM)
            task_list.add_task(task1)
            task_list.add_task(task2)
            storage.save(container)

            # Load and verify
            loaded = storage.load()
            loaded_list = loaded.get_list(task_list.id)
            assert loaded_list.task_count == 2
            assert loaded_list.get_task(task1.id).title == "Fix bug"
            assert loaded_list.get_task(task1.id).priority == Priority.HIGH
            assert loaded_list.get_task(task2.id).priority == Priority.MEDIUM

    def test_save_preserves_task_status(self):
        """Test that task status is preserved through save/load."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)

            # Create and save
            container = ListContainer()
            task_list = container.create_list("Tasks")
            task = Task(title="Test", status=TaskStatus.IN_PROGRESS)
            task_list.add_task(task)
            storage.save(container)

            # Load and verify
            loaded = storage.load()
            loaded_task = loaded.get_list(task_list.id).get_task(task.id)
            assert loaded_task.status == TaskStatus.IN_PROGRESS

    def test_save_preserves_ordering_strategy(self):
        """Test that ordering strategy is preserved."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)

            # Create and save with specific strategy
            container = ListContainer(
                ordering_strategy=OrderingStrategy.ALPHABETICAL
            )
            container.create_list("Zebra")
            container.create_list("Apple")
            storage.save(container)

            # Load and verify
            loaded = storage.load()
            assert loaded.ordering_strategy == OrderingStrategy.ALPHABETICAL


class TestJSONStorageClear:
    """Test clearing storage."""

    def test_clear_deletes_file(self):
        """Test that clear deletes the storage file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)

            # Save
            container = ListContainer()
            container.create_list("Work")
            storage.save(container)
            assert storage.exists() is True

            # Clear
            storage.clear()
            assert storage.exists() is False

    def test_clear_non_existent_file_does_not_error(self):
        """Test that clearing non-existent file doesn't error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)
            storage.clear()  # Should not raise error


class TestJSONStorageInvalidData:
    """Test handling of invalid data."""

    def test_load_corrupted_json_raises_error(self):
        """Test that loading corrupted JSON raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")

            # Write invalid JSON
            with open(file_path, "w") as f:
                f.write("{invalid json")

            storage = JSONStorage(file_path)
            with pytest.raises(ValueError, match="Invalid JSON"):
                storage.load()

    def test_save_and_load_multiple_times(self):
        """Test multiple save/load cycles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)

            # First cycle
            container1 = ListContainer()
            list1 = container1.create_list("List 1")
            storage.save(container1)

            # Second cycle: add more data
            loaded = storage.load()
            list2 = loaded.create_list("List 2")
            storage.save(loaded)

            # Third cycle: verify all data persists
            final = storage.load()
            assert final.list_count == 2


class TestJSONStorageJsonFormat:
    """Test JSON file format."""

    def test_saved_json_is_valid(self):
        """Test that saved JSON is valid and readable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)

            # Save
            container = ListContainer()
            container.create_list("Work")
            storage.save(container)

            # Read and parse JSON directly
            with open(file_path, "r") as f:
                data = json.load(f)

            assert "ordering_strategy" in data
            assert "lists" in data
            assert "metadata" in data

    def test_json_is_readable_format(self):
        """Test that JSON is formatted nicely (indented)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)

            # Save
            container = ListContainer()
            container.create_list("Work")
            storage.save(container)

            # Read file content
            with open(file_path, "r") as f:
                content = f.read()

            # Should have indentation (not minified)
            assert "\n" in content
            assert "  " in content  # 2-space indent


class TestJSONStorageWithTags:
    """Test storage with task tags."""

    def test_save_and_load_tasks_with_tags(self):
        """Test that tags are preserved."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)

            # Create and save
            container = ListContainer()
            task_list = container.create_list("Work")
            task = Task(title="Project", tags=["urgent", "backend"])
            task_list.add_task(task)
            storage.save(container)

            # Load and verify
            loaded = storage.load()
            loaded_task = loaded.get_list(task_list.id).get_task(task.id)
            assert "urgent" in loaded_task.tags
            assert "backend" in loaded_task.tags


class TestJSONStorageFilePermissions:
    """Test file permission handling."""

    def test_save_creates_file(self):
        """Test that save creates the file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "tasks.json")
            storage = JSONStorage(file_path)

            assert not os.path.exists(file_path)

            container = ListContainer()
            storage.save(container)

            assert os.path.exists(file_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
