"""Simple To-Do List CLI - Basic terminal application."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_todo_lib.manager import TaskManager
from my_todo_lib.core.constants import TaskStatus, Priority


def main() -> None:
    """Main entry point for simple to-do CLI."""
    manager = TaskManager()  # Auto-saves to tasks.json by default

    print("=" * 60)
    print("📋 Simple To-Do List CLI")
    print("=" * 60)

    # Create a Work list
    work_list = manager.create_list("Work")
    personal_list = manager.create_list("Personal")

    print(f"\n✅ Created lists: 'Work' and 'Personal'\n")

    # Add some tasks
    print("📝 Adding tasks...")
    manager.add_task_to_list(work_list.id, "Fix production bug", priority=Priority.HIGH)
    manager.add_task_to_list(
        work_list.id, "Review pull requests", description="Review 3 pending PRs"
    )
    manager.add_task_to_list(work_list.id, "Update documentation")

    manager.add_task_to_list(personal_list.id, "Grocery shopping", priority=Priority.MEDIUM)
    manager.add_task_to_list(personal_list.id, "Call mom")
    manager.add_task_to_list(personal_list.id, "Gym session", tags=["health", "daily"])

    # Display all lists
    print("\n📂 All Lists:")
    print("-" * 60)
    for task_list in manager.get_lists():
        print(f"\n  📌 {task_list.name} (ID: {task_list.id})")
        tasks = manager.get_tasks(task_list.id)
        for i, task in enumerate(tasks, 1):
            status_icon = "✓" if task.status == TaskStatus.COMPLETED else "○"
            priority_icon = "🔴" if task.priority == Priority.HIGH else "🟡"
            print(f"     {status_icon} [{priority_icon}] {task.title}")
            if task.description:
                print(f"        📄 {task.description}")
            if task.tags:
                print(f"        🏷️  {', '.join(task.tags)}")

    # Mark some tasks as complete
    print("\n\n⚙️  Marking tasks as complete...")
    tasks = manager.get_tasks(work_list.id)
    if tasks:
        # Mark first task as IN_PROGRESS
        manager.update_task(work_list.id, tasks[0].id, status=TaskStatus.IN_PROGRESS)
        print(f"   ➜ Marked '{tasks[0].title}' as IN_PROGRESS")

        # Mark second task as COMPLETED
        if len(tasks) > 1:
            manager.update_task(work_list.id, tasks[1].id, status=TaskStatus.COMPLETED)
            print(f"   ✅ Marked '{tasks[1].title}' as COMPLETED")

    # Display statistics
    print("\n\n📊 Statistics:")
    print("-" * 60)
    stats = manager.get_statistics()
    print(f"  Total Lists: {stats['total_lists']}")
    print(f"  Total Tasks: {stats['total_tasks']}")
    print(f"  ✓ Completed: {stats['completed_tasks']}")
    print(f"  → In Progress: {stats['in_progress_tasks']}")
    print(f"  ○ To Do: {stats['todo_tasks']}")
    print(f"  📈 Completion: {stats['completion_percentage']}%")

    # Search example
    print("\n\n🔍 Search Example - Finding 'bug':")
    print("-" * 60)
    results = manager.search_tasks_across_lists("bug")
    if results:
        for task_list, task in results:
            print(f"  Found in '{task_list.name}': {task.title}")
    else:
        print("  No tasks found with 'bug'")

    # Data persistence
    print("\n\n💾 Data Saved!")
    print("   All changes automatically saved to 'tasks.json'")
    print("   Run this script again to see your data persist!")

    print("\n" + "=" * 60)
    print("✨ Demo Complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
