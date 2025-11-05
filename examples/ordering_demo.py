"""Multi-List Ordering Example - Demonstrating different list orderings."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_todo_lib.manager import TaskManager
from my_todo_lib.core.constants import OrderingStrategy


def main() -> None:
    """Demonstrate different list ordering strategies."""
    print("=" * 70)
    print("🔄 Multi-List Ordering Strategies Demo")
    print("=" * 70)

    # Create a fresh manager for this demo
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        from my_todo_lib.storage.json_storage import JSONStorage
        storage = JSONStorage(os.path.join(tmpdir, "ordering_demo.json"))
        manager = TaskManager(storage=storage)

        # Create lists in random order
        print("\n📋 Creating lists: Zebra, Apple, Banana, Cherry")
        print("-" * 70)
        
        zebra = manager.create_list("Zebra")
        manager.add_task_to_list(zebra.id, "Task 1")

        apple = manager.create_list("Apple")
        manager.add_task_to_list(apple.id, "Task 1")

        banana = manager.create_list("Banana")
        manager.add_task_to_list(banana.id, "Task 1")

        cherry = manager.create_list("Cherry")
        manager.add_task_to_list(cherry.id, "Task 1")

        # Display with MANUAL ordering (insertion order)
        print("\n1️⃣  MANUAL Strategy (Insertion Order):")
        print("-" * 70)
        manager.set_list_ordering(OrderingStrategy.MANUAL)
        for i, task_list in enumerate(manager.get_lists(), 1):
            print(f"   {i}. {task_list.name}")

        # Display with ALPHABETICAL ordering
        print("\n2️⃣  ALPHABETICAL Strategy:")
        print("-" * 70)
        manager.set_list_ordering(OrderingStrategy.ALPHABETICAL)
        for i, task_list in enumerate(manager.get_lists(), 1):
            print(f"   {i}. {task_list.name}")

        # Switch back to MANUAL and demonstrate moving
        print("\n3️⃣  MANUAL Strategy - After Moving Zebra to position 3:")
        print("-" * 70)
        manager.set_list_ordering(OrderingStrategy.MANUAL)
        manager.move_list(zebra.id, 2)  # Move to index 2 (3rd position)
        for i, task_list in enumerate(manager.get_lists(), 1):
            print(f"   {i}. {task_list.name}")

        # Add more tasks to show RECENTLY_ADDED_TASK ordering
        print("\n4️⃣  Adding tasks to demonstrate ordering...")
        print("-" * 70)
        manager.add_task_to_list(cherry.id, "New task in Cherry")
        manager.add_task_to_list(apple.id, "New task in Apple")
        
        print("\n5️⃣  RECENTLY_ADDED_TASK Strategy:")
        print("-" * 70)
        manager.set_list_ordering(OrderingStrategy.RECENTLY_ADDED_TASK)
        for i, task_list in enumerate(manager.get_lists(), 1):
            task_count = len(manager.get_tasks(task_list.id))
            print(f"   {i}. {task_list.name} ({task_count} tasks)")

        # Show CREATION_ORDER
        print("\n6️⃣  CREATION_ORDER Strategy (same as insertion for this demo):")
        print("-" * 70)
        manager.set_list_ordering(OrderingStrategy.CREATION_ORDER)
        for i, task_list in enumerate(manager.get_lists(), 1):
            print(f"   {i}. {task_list.name}")

        # Show how ordering persists
        print("\n💾 Saving and reloading to verify persistence...")
        manager.save()
        
        # Load from saved data
        manager2 = TaskManager(storage=storage)
        manager2.load()
        
        print("\n7️⃣  Loaded state (should match above):")
        print("-" * 70)
        for i, task_list in enumerate(manager2.get_lists(), 1):
            print(f"   {i}. {task_list.name}")

    print("\n" + "=" * 70)
    print("✨ Ordering Demo Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
