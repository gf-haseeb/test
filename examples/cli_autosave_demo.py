"""
Demonstration that the interactive CLI auto-saves all changes to tasks.json.
This script simulates what happens when you use the interactive CLI.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_todo_lib.manager import TaskManager
from my_todo_lib.core.constants import TaskStatus, Priority
from my_todo_lib.storage.json_storage import JSONStorage

def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")

def print_json_snapshot(filename: str, label: str) -> None:
    """Print current JSON file snapshot."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        
        print(f"📄 {label}:")
        print("-" * 70)
        
        # Summary
        list_count = len(data['lists'])
        total_tasks = sum(len(lst['tasks']) for lst in data['lists'])
        ordering = data['ordering_strategy']
        
        print(f"  📂 Lists: {list_count}")
        print(f"  📋 Total Tasks: {total_tasks}")
        print(f"  🔄 Ordering: {ordering}")
        
        # Details
        for lst in data['lists']:
            completed = sum(1 for t in lst['tasks'] if t['status'] == 'completed')
            print(f"\n  List: '{lst['name']}' (ID: {lst['id']})")
            print(f"    Tasks: {len(lst['tasks'])}, Completed: {completed}")
            for task in lst['tasks']:
                status_icon = "✓" if task['status'] == 'completed' else "○"
                priority_emoji = "🔴" if task['priority'] == 'high' else (
                    "🟡" if task['priority'] == 'medium' else "🟢"
                )
                print(f"      {status_icon} [{priority_emoji}] {task['title']}")
    else:
        print(f"❌ {filename} does not exist yet")

def simulate_cli_usage():
    """Simulate typical interactive CLI usage patterns."""
    
    json_file = "demo_tasks.json"
    
    # Clean up if exists
    if os.path.exists(json_file):
        os.remove(json_file)
    
    print_section("🎬 INTERACTIVE CLI AUTO-SAVE DEMONSTRATION")
    print(f"Using JSON file: {json_file}\n")
    
    # Initialize manager
    manager = TaskManager(storage=JSONStorage(json_file))
    
    # SCENARIO 1: User creates lists and adds tasks
    print_section("SCENARIO 1: Creating Lists and Tasks")
    print("User Actions:")
    print("  1. Create 'Work' list")
    print("  2. Add 3 tasks to Work list")
    print("  3. Create 'Personal' list")
    print()
    
    # Create lists
    work_list = manager.create_list("Work", "Work-related tasks")
    print(f"✅ Created list: Work (ID: {work_list.id})")
    
    personal_list = manager.create_list("Personal", "Personal tasks")
    print(f"✅ Created list: Personal (ID: {personal_list.id})")
    
    # Add tasks to work list
    t1 = manager.add_task_to_list(
        work_list.id,
        title="Finish documentation",
        priority=Priority.HIGH
    )
    print("✅ Added task: Finish documentation")
    
    _ = manager.add_task_to_list(
        work_list.id,
        title="Review pull requests",
        priority=Priority.MEDIUM,
        tags=["review"]
    )
    print("✅ Added task: Review pull requests")
    
    t3 = manager.add_task_to_list(
        work_list.id,
        title="Team meeting",
        priority=Priority.MEDIUM
    )
    print("✅ Added task: Team meeting")
    
    print_json_snapshot(json_file, "JSON State After Adding Tasks")
    
    # SCENARIO 2: User marks tasks as complete
    print_section("SCENARIO 2: Updating Task Status")
    print("User Actions:")
    print("  1. Mark 'Team meeting' as IN_PROGRESS")
    print("  2. Mark 'Finish documentation' as COMPLETED")
    print()
    
    manager.update_task(work_list.id, t3.id, status=TaskStatus.IN_PROGRESS)
    print("✅ Updated: Team meeting → IN_PROGRESS")
    
    manager.update_task(work_list.id, t1.id, status=TaskStatus.COMPLETED)
    print("✅ Updated: Finish documentation → COMPLETED")
    
    print_json_snapshot(json_file, "JSON State After Updating Status")
    
    # SCENARIO 3: User adds tasks to personal list
    print_section("SCENARIO 3: Adding Tasks to Personal List")
    print("User Actions:")
    print("  1. Add 'Buy groceries' to Personal")
    print("  2. Add 'Exercise' to Personal")
    print()
    
    p1 = manager.add_task_to_list(
        personal_list.id,
        title="Buy groceries",
        priority=Priority.LOW
    )
    print("✅ Added task: Buy groceries")
    
    _ = manager.add_task_to_list(
        personal_list.id,
        title="Exercise 30 minutes",
        priority=Priority.HIGH,
        tags=["health", "daily"]
    )
    print("✅ Added task: Exercise 30 minutes")
    
    print_json_snapshot(json_file, "JSON State After Personal Tasks")
    
    # SCENARIO 4: User deletes and renames
    print_section("SCENARIO 4: Renaming and Deleting")
    print("User Actions:")
    print("  1. Rename Work list to 'Work - Sprint 1'")
    print("  2. Delete 'Buy groceries' task")
    print()
    
    manager.rename_list(work_list.id, "Work - Sprint 1")
    print("✅ Renamed: Work → Work - Sprint 1")
    
    manager.delete_task(personal_list.id, p1.id)
    print("✅ Deleted task: Buy groceries")
    
    print_json_snapshot(json_file, "JSON State After Rename/Delete")
    
    # SCENARIO 5: Statistics
    print_section("SCENARIO 5: Final Statistics")
    stats = manager.get_statistics()
    
    print("Overall Statistics:")
    print(f"  📂 Total Lists: {stats['total_lists']}")
    print(f"  📋 Total Tasks: {stats['total_tasks']}")
    print(f"  ✓ Completed: {stats['completed_tasks']}")
    print(f"  → In Progress: {stats['in_progress_tasks']}")
    print(f"  ○ To Do: {stats['todo_tasks']}")
    print(f"  📈 Completion %: {stats['completion_percentage']:.1f}%")
    
    print_json_snapshot(json_file, "Final JSON File Content")
    
    # Final summary
    print_section("✅ DEMONSTRATION COMPLETE")
    print("Key Points:")
    print("  ✓ JSON file created automatically")
    print("  ✓ Every action is immediately saved")
    print("  ✓ File is ready to be loaded on next session")
    print("  ✓ All data types properly serialized")
    print(f"\nJSON file saved at: {os.path.abspath(json_file)}")
    
    # Keep the file for inspection
    print(f"\n💡 Tip: You can inspect '{json_file}' with any text editor")

if __name__ == "__main__":
    simulate_cli_usage()
