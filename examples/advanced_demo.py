"""Advanced Example - Search, Filter, and Statistics."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_todo_lib.manager import TaskManager
from my_todo_lib.core.constants import TaskStatus, Priority


def main() -> None:
    """Demonstrate search, filtering, and advanced features."""
    print("=" * 70)
    print("🔎 Advanced Features: Search, Filter & Analytics")
    print("=" * 70)

    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        from my_todo_lib.storage.json_storage import JSONStorage
        storage = JSONStorage(os.path.join(tmpdir, "advanced_demo.json"))
        manager = TaskManager(storage=storage)

        # Setup: Create realistic project structure
        print("\n📂 Setting up project lists and tasks...")
        print("-" * 70)

        # Backend list
        backend = manager.create_list("Backend API")
        manager.add_task_to_list(
            backend.id,
            "Fix database connection pool",
            description="Optimize connection handling",
            priority=Priority.HIGH,
            tags=["database", "urgent", "performance"]
        )
        manager.add_task_to_list(
            backend.id,
            "Implement caching layer",
            description="Add Redis caching for expensive queries",
            priority=Priority.HIGH,
            tags=["performance", "redis", "optimization"]
        )
        manager.add_task_to_list(
            backend.id,
            "Write API tests",
            priority=Priority.MEDIUM,
            tags=["testing", "ci-cd"]
        )

        # Frontend list
        frontend = manager.create_list("Frontend UI")
        manager.add_task_to_list(
            frontend.id,
            "Design dark mode theme",
            description="Implement dark mode UI components",
            priority=Priority.MEDIUM,
            tags=["ui", "design", "theme"]
        )
        manager.add_task_to_list(
            frontend.id,
            "Fix responsive design bugs",
            priority=Priority.HIGH,
            tags=["bug", "mobile", "responsive"]
        )
        manager.add_task_to_list(
            frontend.id,
            "Add accessibility features",
            priority=Priority.LOW,
            tags=["accessibility", "a11y"]
        )

        # DevOps list
        devops = manager.create_list("DevOps")
        manager.add_task_to_list(
            devops.id,
            "Setup CI/CD pipeline",
            priority=Priority.HIGH,
            tags=["ci-cd", "deployment", "urgent"]
        )
        manager.add_task_to_list(
            devops.id,
            "Monitor database performance",
            priority=Priority.MEDIUM,
            tags=["monitoring", "database"]
        )

        print("✅ Created 3 lists with 8 tasks total\n")

        # Feature 1: Search
        print("\n🔍 SEARCH EXAMPLES:")
        print("-" * 70)

        search_terms = ["database", "bug", "performance"]
        for term in search_terms:
            results = manager.search_tasks_across_lists(term)
            print(f"\n  Searching for '{term}':")
            if results:
                for task_list, task in results:
                    print(f"    • {task_list.name}: {task.title}")
            else:
                print(f"    • No results found")

        # Feature 2: Filter by priority
        print("\n\n🎯 FILTER BY PRIORITY:")
        print("-" * 70)

        for priority in [Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            high_priority_tasks = []
            for task_list in manager.get_lists():
                tasks = manager.get_tasks(task_list.id, status=None)
                for task in tasks:
                    if task.priority == priority:
                        high_priority_tasks.append((task_list, task))

            if high_priority_tasks:
                print(f"\n  {priority.value.upper()} Priority Tasks:")
                for task_list, task in high_priority_tasks:
                    status_icon = "✓" if task.status == TaskStatus.COMPLETED else "○"
                    print(f"    {status_icon} [{task_list.name}] {task.title}")

        # Feature 3: Tag-based search
        print("\n\n🏷️  SEARCH BY TAGS:")
        print("-" * 70)

        tags_to_search = ["database", "performance", "urgent"]
        for tag in tags_to_search:
            results = manager.search_tasks_across_lists(tag, search_in="tags")
            print(f"\n  Tasks tagged with '{tag}':")
            if results:
                for task_list, task in results:
                    print(f"    • {task_list.name}: {task.title}")
            else:
                print(f"    • No tasks found")

        # Feature 4: Update task status
        print("\n\n📊 UPDATING TASK STATUS:")
        print("-" * 70)

        tasks = manager.get_tasks(backend.id)
        if tasks:
            task = tasks[0]
            print(f"\n  Before: {task.title}")
            print(f"    Status: {task.status.value}")
            
            manager.update_task(backend.id, task.id, status=TaskStatus.IN_PROGRESS)
            updated = manager.get_task(backend.id, task.id)
            print(f"\n  After: {updated.title}")
            print(f"    Status: {updated.status.value}")

        # Feature 5: Statistics and Analytics
        print("\n\n📈 FULL PROJECT STATISTICS:")
        print("-" * 70)

        stats = manager.get_statistics()
        print(f"\n  Overview:")
        print(f"    📂 Lists: {stats['total_lists']}")
        print(f"    ✓ Total Tasks: {stats['total_tasks']}")
        print(f"\n  Status Breakdown:")
        print(f"    ✓ Completed: {stats['completed_tasks']}")
        print(f"    → In Progress: {stats['in_progress_tasks']}")
        print(f"    ○ To Do: {stats['todo_tasks']}")
        print(f"\n  Progress: {stats['completion_percentage']}%")

        # Feature 6: Per-list statistics
        print("\n\n📋 PER-LIST BREAKDOWN:")
        print("-" * 70)

        for task_list in manager.get_lists():
            tasks = manager.get_tasks(task_list.id)
            completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
            in_progress = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
            todo = sum(1 for t in tasks if t.status == TaskStatus.TODO)

            print(f"\n  {task_list.name}:")
            print(f"    ✓ Completed: {completed}")
            print(f"    → In Progress: {in_progress}")
            print(f"    ○ To Do: {todo}")
            print(f"    Total: {len(tasks)}")

        # Feature 7: Delete and cleanup
        print("\n\n🗑️  CLEANUP EXAMPLE:")
        print("-" * 70)

        tasks = manager.get_tasks(frontend.id)
        if tasks:
            task_to_delete = tasks[-1]
            print(f"\n  Deleting task: {task_to_delete.title}")
            manager.delete_task(frontend.id, task_to_delete.id)
            
            remaining = manager.get_tasks(frontend.id)
            print(f"  Remaining tasks in '{frontend.name}': {len(remaining)}")

    print("\n" + "=" * 70)
    print("✨ Advanced Demo Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
