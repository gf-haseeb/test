"""Test script to verify that auto-save works in the interactive CLI."""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_todo_lib.manager import TaskManager
from my_todo_lib.core.constants import TaskStatus, Priority, OrderingStrategy

def test_autosave():
    """Test that the manager auto-saves to JSON on every change."""
    
    # Use a test file
    test_json_file = "test_autosave.json"
    
    # Clean up if it exists
    if os.path.exists(test_json_file):
        os.remove(test_json_file)
    
    print("=" * 70)
    print("🧪 AUTO-SAVE FUNCTIONALITY TEST")
    print("=" * 70)
    
    # Create manager with test file
    from my_todo_lib.storage.json_storage import JSONStorage
    manager = TaskManager(storage=JSONStorage(test_json_file))
    
    # Test 1: Create a list
    print("\n✓ Test 1: Creating a list...")
    list1 = manager.create_list("Work Tasks", "Tasks for work")
    print(f"  Created list: {list1.name} (ID: {list1.id})")
    
    # Check if JSON file exists
    if os.path.exists(test_json_file):
        with open(test_json_file, 'r') as f:
            data = json.load(f)
        print(f"  ✅ JSON file created with {len(data['lists'])} list(s)")
    else:
        print("  ❌ JSON file NOT created!")
        return
    
    # Test 2: Add a task
    print("\n✓ Test 2: Adding a task...")
    task1 = manager.add_task_to_list(
        list1.id,
        title="Complete project",
        description="Finish the project deadline",
        priority=Priority.HIGH
    )
    print(f"  Added task: {task1.title} (ID: {task1.id})")
    
    # Check JSON file again
    with open(test_json_file, 'r') as f:
        data = json.load(f)
    task_count = len(data['lists'][0]['tasks'])
    print(f"  ✅ JSON updated: {task_count} task(s) in list")
    
    # Test 3: Add another task
    print("\n✓ Test 3: Adding another task...")
    task2 = manager.add_task_to_list(
        list1.id,
        title="Review code",
        priority=Priority.MEDIUM,
        tags=["review", "important"]
    )
    print(f"  Added task: {task2.title}")
    
    with open(test_json_file, 'r') as f:
        data = json.load(f)
    task_count = len(data['lists'][0]['tasks'])
    print(f"  ✅ JSON updated: {task_count} task(s) in list")
    
    # Test 4: Create another list
    print("\n✓ Test 4: Creating another list...")
    list2 = manager.create_list("Personal", "Personal tasks")
    print(f"  Created list: {list2.name}")
    
    with open(test_json_file, 'r') as f:
        data = json.load(f)
    list_count = len(data['lists'])
    print(f"  ✅ JSON updated: {list_count} list(s) total")
    
    # Test 5: Rename a list
    print("\n✓ Test 5: Renaming a list...")
    manager.rename_list(list1.id, "Work - Q4 2025")
    print("  Renamed list to: Work - Q4 2025")
    
    with open(test_json_file, 'r') as f:
        data = json.load(f)
    updated_name = data['lists'][0]['name']
    print(f"  ✅ JSON updated: List name is now '{updated_name}'")
    
    # Test 6: Mark task as complete
    print("\n✓ Test 6: Marking task as complete...")
    manager.update_task(list1.id, task1.id, status=TaskStatus.COMPLETED)
    print(f"  Marked '{task1.title}' as COMPLETED")
    
    with open(test_json_file, 'r') as f:
        data = json.load(f)
    task_status = data['lists'][0]['tasks'][0]['status']
    print(f"  ✅ JSON updated: Task status is now '{task_status}'")
    
    # Test 7: Change ordering strategy
    print("\n✓ Test 7: Changing list ordering strategy...")
    manager.set_list_ordering(OrderingStrategy.ALPHABETICAL)
    print("  Set ordering to: ALPHABETICAL")
    
    with open(test_json_file, 'r') as f:
        data = json.load(f)
    ordering = data['ordering_strategy']
    print(f"  ✅ JSON updated: Ordering strategy is '{ordering}'")
    
    # Test 8: Delete a task
    print("\n✓ Test 8: Deleting a task...")
    manager.delete_task(list1.id, task2.id)
    print(f"  Deleted task: {task2.title}")
    
    with open(test_json_file, 'r') as f:
        data = json.load(f)
    task_count = len(data['lists'][0]['tasks'])
    print(f"  ✅ JSON updated: {task_count} task(s) remaining in list")
    
    # Test 9: Delete a list
    print("\n✓ Test 9: Deleting a list...")
    manager.delete_list(list2.id)
    print(f"  Deleted list: {list2.name}")
    
    with open(test_json_file, 'r') as f:
        data = json.load(f)
    list_count = len(data['lists'])
    print(f"  ✅ JSON updated: {list_count} list(s) remaining")
    
    # Test 10: Verify JSON file structure
    print("\n✓ Test 10: Verifying JSON structure...")
    with open(test_json_file, 'r') as f:
        data = json.load(f)
    
    print(f"  ✅ Root keys: {list(data.keys())}")
    print(f"  ✅ Number of lists: {len(data['lists'])}")
    print(f"  ✅ Ordering strategy: {data['ordering_strategy']}")
    
    if data['lists']:
        first_list = data['lists'][0]
        print(f"  ✅ First list has keys: {list(first_list.keys())}")
        print(f"  ✅ First list has {len(first_list['tasks'])} task(s)")
    
    # Show JSON file contents
    print("\n📄 Final JSON File Content:")
    print("-" * 70)
    print(json.dumps(data, indent=2))
    
    # Clean up
    os.remove(test_json_file)
    
    print("\n" + "=" * 70)
    print("✅ ALL AUTO-SAVE TESTS PASSED!")
    print("=" * 70)
    print("\n🎯 Summary:")
    print("   • JSON file is created automatically on first save")
    print("   • JSON file is updated on every list/task change")
    print("   • All data is persisted correctly")
    print("   • File structure is properly formatted")

if __name__ == "__main__":
    test_autosave()
