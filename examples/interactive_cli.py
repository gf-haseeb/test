"""Interactive To-Do List CLI - Full-featured terminal application."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_todo_lib.manager import TaskManager
from my_todo_lib.core.constants import TaskStatus, Priority, OrderingStrategy


class TodoCLI:
    """Interactive CLI for the to-do list manager."""

    def __init__(self) -> None:
        """Initialize the CLI."""
        self.manager = TaskManager()
        self.current_list_id: int = None
        self.running = True

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system("clear" if os.name == "posix" else "cls")

    def print_header(self, title: str) -> None:
        """Print a formatted header."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)

    def print_menu(self, options: dict) -> None:
        """Print a menu with options."""
        for key, label in options.items():
            print(f"  {key}. {label}")
        print()

    def get_input(self, prompt: str = "> ") -> str:
        """Get user input."""
        return input(f"\n{prompt}").strip()

    def show_main_menu(self) -> None:
        """Display main menu."""
        self.clear_screen()
        self.print_header("📋 To-Do List Manager")

        options = {
            "1": "📂 Manage Lists",
            "2": "✏️  Manage Tasks",
            "3": "🔍 Search Tasks",
            "4": "📊 View Statistics",
            "5": "⚙️  Settings",
            "6": "❌ Exit",
        }

        self.print_menu(options)
        choice = self.get_input("Select option: ")

        actions = {
            "1": self.list_management_menu,
            "2": self.task_management_menu,
            "3": self.search_menu,
            "4": self.view_statistics,
            "5": self.settings_menu,
            "6": self.exit_app,
        }

        if choice in actions:
            actions[choice]()
        else:
            print("❌ Invalid option. Please try again.")
            input("Press Enter to continue...")

    def list_management_menu(self) -> None:
        """List management menu."""
        self.clear_screen()
        self.print_header("📂 List Management")

        options = {
            "1": "View all lists",
            "2": "Create new list",
            "3": "Select list to work with",
            "4": "Rename list",
            "5": "Delete list",
            "6": "Change list ordering",
            "7": "Back to main menu",
        }

        self.print_menu(options)
        choice = self.get_input("Select option: ")

        actions = {
            "1": self.view_lists,
            "2": self.create_list,
            "3": self.select_list,
            "4": self.rename_list,
            "5": self.delete_list,
            "6": self.change_ordering,
            "7": self.show_main_menu,
        }

        if choice in actions:
            actions[choice]()
        else:
            print("❌ Invalid option.")
            input("Press Enter to continue...")
            self.list_management_menu()

    def view_lists(self) -> None:
        """Display all lists."""
        lists = self.manager.get_lists()

        if not lists:
            print("\n📭 No lists yet. Create one!")
            input("Press Enter to continue...")
            return

        print("\n📂 All Lists:")
        print("-" * 70)
        for i, task_list in enumerate(lists, 1):
            tasks = self.manager.get_tasks(task_list.id)
            completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
            print(
                f"  {i}. {task_list.name} (ID: {task_list.id}) "
                f"- {len(tasks)} tasks, {completed} completed"
            )

        input("\nPress Enter to continue...")
        self.list_management_menu()

    def create_list(self) -> None:
        """Create a new list."""
        print("\n📝 Create New List")
        print("-" * 70)
        name = self.get_input("List name: ")

        if not name:
            print("❌ List name cannot be empty.")
            input("Press Enter to continue...")
            return

        description = self.get_input("Description (optional): ")
        new_list = self.manager.create_list(name, description)

        print(f"\n✅ List '{new_list.name}' created successfully! (ID: {new_list.id})")
        input("Press Enter to continue...")
        self.list_management_menu()

    def select_list(self) -> None:
        """Select a list to work with."""
        lists = self.manager.get_lists()

        if not lists:
            print("\n📭 No lists available.")
            input("Press Enter to continue...")
            return

        print("\n📂 Select List:")
        print("-" * 70)
        for i, task_list in enumerate(lists, 1):
            print(f"  {i}. {task_list.name}")

        try:
            choice = int(self.get_input("Select list number: "))
            if 1 <= choice <= len(lists):
                self.current_list_id = lists[choice - 1].id
                print(f"\n✅ Selected: {lists[choice - 1].name}")
                input("Press Enter to continue...")
                self.task_management_menu()
            else:
                print("❌ Invalid selection.")
                input("Press Enter to continue...")
                self.select_list()
        except ValueError:
            print("❌ Please enter a number.")
            input("Press Enter to continue...")
            self.select_list()

    def rename_list(self) -> None:
        """Rename a list."""
        lists = self.manager.get_lists()

        if not lists:
            print("\n📭 No lists to rename.")
            input("Press Enter to continue...")
            return

        print("\n✏️  Rename List")
        print("-" * 70)
        for i, task_list in enumerate(lists, 1):
            print(f"  {i}. {task_list.name}")

        try:
            choice = int(self.get_input("Select list number: "))
            if 1 <= choice <= len(lists):
                list_id = lists[choice - 1].id
                new_name = self.get_input("New name: ")
                if new_name:
                    self.manager.rename_list(list_id, new_name)
                    print(f"\n✅ List renamed to '{new_name}'")
                input("Press Enter to continue...")
                self.list_management_menu()
            else:
                print("❌ Invalid selection.")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a number.")
            input("Press Enter to continue...")

    def delete_list(self) -> None:
        """Delete a list."""
        lists = self.manager.get_lists()

        if not lists:
            print("\n📭 No lists to delete.")
            input("Press Enter to continue...")
            return

        print("\n🗑️  Delete List")
        print("-" * 70)
        for i, task_list in enumerate(lists, 1):
            print(f"  {i}. {task_list.name}")

        try:
            choice = int(self.get_input("Select list number to delete: "))
            if 1 <= choice <= len(lists):
                list_id = lists[choice - 1].id
                confirm = self.get_input("Are you sure? (yes/no): ").lower()
                if confirm == "yes":
                    self.manager.delete_list(list_id)
                    print("\n✅ List deleted!")
                    if self.current_list_id == list_id:
                        self.current_list_id = None
                input("Press Enter to continue...")
                self.list_management_menu()
            else:
                print("❌ Invalid selection.")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a number.")
            input("Press Enter to continue...")

    def change_ordering(self) -> None:
        """Change list ordering strategy."""
        print("\n🔄 Change List Ordering")
        print("-" * 70)

        strategies = {
            "1": OrderingStrategy.MANUAL,
            "2": OrderingStrategy.ALPHABETICAL,
            "3": OrderingStrategy.CREATION_ORDER,
            "4": OrderingStrategy.RECENTLY_MODIFIED,
            "5": OrderingStrategy.RECENTLY_ADDED_TASK,
        }

        options = {
            "1": "Manual (custom order)",
            "2": "Alphabetical (A-Z)",
            "3": "Creation order",
            "4": "Recently modified",
            "5": "Recently added task",
        }

        self.print_menu(options)

        choice = self.get_input("Select ordering: ")
        if choice in strategies:
            self.manager.set_list_ordering(strategies[choice])
            print(f"\n✅ Ordering changed to {strategies[choice].value}")
            input("Press Enter to continue...")
            self.list_management_menu()
        else:
            print("❌ Invalid option.")
            input("Press Enter to continue...")
            self.change_ordering()

    def task_management_menu(self) -> None:
        """Task management menu."""
        if self.current_list_id is None:
            lists = self.manager.get_lists()
            if lists:
                print("\n⚠️  No list selected. Please select a list first.")
                input("Press Enter to continue...")
                self.select_list()
            else:
                print("\n❌ No lists available. Create one first!")
                input("Press Enter to continue...")
                self.list_management_menu()
            return

        current_list = self.manager.get_list(self.current_list_id)
        self.clear_screen()
        self.print_header(f"✏️  Task Management - {current_list.name}")

        options = {
            "1": "View all tasks",
            "2": "Add new task",
            "3": "Mark task complete",
            "4": "Update task",
            "5": "Delete task",
            "6": "Move task to another list",
            "7": "Filter tasks",
            "8": "Back to main menu",
        }

        self.print_menu(options)
        choice = self.get_input("Select option: ")

        actions = {
            "1": self.view_tasks,
            "2": self.add_task,
            "3": self.mark_complete,
            "4": self.update_task,
            "5": self.delete_task,
            "6": self.move_task,
            "7": self.filter_tasks,
            "8": self.show_main_menu,
        }

        if choice in actions:
            actions[choice]()
        else:
            print("❌ Invalid option.")
            input("Press Enter to continue...")
            self.task_management_menu()

    def view_tasks(self) -> None:
        """View all tasks in current list."""
        tasks = self.manager.get_tasks(self.current_list_id)

        if not tasks:
            print("\n📭 No tasks in this list.")
            input("Press Enter to continue...")
            self.task_management_menu()
            return

        print("\n📋 Tasks:")
        print("-" * 70)
        for i, task in enumerate(tasks, 1):
            status_icon = "✓" if task.status == TaskStatus.COMPLETED else "○"
            priority_icon = "🔴" if task.priority == Priority.HIGH else (
                "🟡" if task.priority == Priority.MEDIUM else "🟢"
            )
            tags_str = f" | Tags: {', '.join(task.tags)}" if task.tags else ""
            print(f"  {i}. {status_icon} [{priority_icon}] {task.title} (ID: {task.id}){tags_str}")
            if task.description:
                print(f"     📄 {task.description}")

        input("\nPress Enter to continue...")
        self.task_management_menu()

    def add_task(self) -> None:
        """Add a new task."""
        print("\n➕ Add New Task")
        print("-" * 70)
        title = self.get_input("Task title: ")

        if not title:
            print("❌ Task title cannot be empty.")
            input("Press Enter to continue...")
            return

        description = self.get_input("Description (optional): ")

        print("\nPriority: (1) Low  (2) Medium  (3) High")
        priority_choice = self.get_input("Priority [2]: ").strip() or "2"
        priority_map = {"1": Priority.LOW, "2": Priority.MEDIUM, "3": Priority.HIGH}
        priority = priority_map.get(priority_choice, Priority.MEDIUM)

        tags_input = self.get_input("Tags (comma-separated, optional): ")
        tags = [t.strip() for t in tags_input.split(",")] if tags_input else None

        task = self.manager.add_task_to_list(
            self.current_list_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
        )

        print(f"\n✅ Task '{task.title}' added!")
        input("Press Enter to continue...")
        self.task_management_menu()

    def mark_complete(self) -> None:
        """Mark a task as complete."""
        tasks = self.manager.get_tasks(self.current_list_id)

        if not tasks:
            print("\n📭 No tasks to complete.")
            input("Press Enter to continue...")
            return

        print("\n✅ Mark Task Complete")
        print("-" * 70)
        for i, task in enumerate(tasks, 1):
            status = "✓" if task.status == TaskStatus.COMPLETED else "○"
            print(f"  {i}. {status} {task.title}")

        try:
            choice = int(self.get_input("Select task number: "))
            if 1 <= choice <= len(tasks):
                task = tasks[choice - 1]
                self.manager.update_task(
                    self.current_list_id,
                    task.id,
                    status=TaskStatus.COMPLETED,
                )
                print(f"\n✅ '{task.title}' marked as complete!")
                input("Press Enter to continue...")
                self.task_management_menu()
            else:
                print("❌ Invalid selection.")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a number.")
            input("Press Enter to continue...")

    def update_task(self) -> None:
        """Update task details."""
        tasks = self.manager.get_tasks(self.current_list_id)

        if not tasks:
            print("\n📭 No tasks to update.")
            input("Press Enter to continue...")
            return

        print("\n✏️  Update Task")
        print("-" * 70)
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task.title} ({task.status.value})")

        try:
            choice = int(self.get_input("Select task number: "))
            if 1 <= choice <= len(tasks):
                task = tasks[choice - 1]

                print(f"\nUpdating: {task.title}")
                print("(Leave blank to keep current value)")
                print("-" * 70)

                new_status_input = self.get_input(
                    f"Status (1=TODO, 2=IN_PROGRESS, 3=COMPLETED) [{task.status.value}]: "
                ).strip()

                new_priority_input = self.get_input(
                    f"Priority (1=LOW, 2=MEDIUM, 3=HIGH) [{task.priority.value}]: "
                ).strip()

                updates = {}

                if new_status_input:
                    status_map = {
                        "1": TaskStatus.TODO,
                        "2": TaskStatus.IN_PROGRESS,
                        "3": TaskStatus.COMPLETED,
                    }
                    updates["status"] = status_map.get(new_status_input, task.status)

                if new_priority_input:
                    priority_map = {
                        "1": Priority.LOW,
                        "2": Priority.MEDIUM,
                        "3": Priority.HIGH,
                    }
                    updates["priority"] = priority_map.get(new_priority_input, task.priority)

                if updates:
                    self.manager.update_task(self.current_list_id, task.id, **updates)
                    print("\n✅ Task updated!")
                else:
                    print("\n⚠️  No changes made.")

                input("Press Enter to continue...")
                self.task_management_menu()
            else:
                print("❌ Invalid selection.")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a number.")
            input("Press Enter to continue...")

    def delete_task(self) -> None:
        """Delete a task."""
        tasks = self.manager.get_tasks(self.current_list_id)

        if not tasks:
            print("\n📭 No tasks to delete.")
            input("Press Enter to continue...")
            return

        print("\n🗑️  Delete Task")
        print("-" * 70)
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task.title}")

        try:
            choice = int(self.get_input("Select task number to delete: "))
            if 1 <= choice <= len(tasks):
                task = tasks[choice - 1]
                confirm = self.get_input(f"Delete '{task.title}'? (yes/no): ").lower()
                if confirm == "yes":
                    self.manager.delete_task(self.current_list_id, task.id)
                    print("\n✅ Task deleted!")
                input("Press Enter to continue...")
                self.task_management_menu()
            else:
                print("❌ Invalid selection.")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a number.")
            input("Press Enter to continue...")

    def move_task(self) -> None:
        """Move a task to another list."""
        tasks = self.manager.get_tasks(self.current_list_id)

        if not tasks:
            print("\n📭 No tasks to move.")
            input("Press Enter to continue...")
            return

        print("\n📦 Move Task to Another List")
        print("-" * 70)
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task.title}")

        try:
            choice = int(self.get_input("Select task number to move: "))
            if 1 <= choice <= len(tasks):
                task = tasks[choice - 1]

                # Show available lists
                all_lists = self.manager.get_lists()
                other_lists = [lst for lst in all_lists if lst.id != self.current_list_id]

                if not other_lists:
                    print("\n❌ No other lists available. Create a new list first!")
                    input("Press Enter to continue...")
                    return

                print("\n📂 Available Lists:")
                print("-" * 70)
                for i, lst in enumerate(other_lists, 1):
                    print(f"  {i}. {lst.name}")
                print(f"  {len(other_lists) + 1}. Create new list and move")

                target_choice = self.get_input("Select target list or create new: ")

                if target_choice == str(len(other_lists) + 1):
                    # Create new list
                    new_list_name = self.get_input("New list name: ")
                    if not new_list_name:
                        print("❌ List name cannot be empty.")
                        input("Press Enter to continue...")
                        return

                    new_list = self.manager.create_list(new_list_name)
                    target_list_id = new_list.id
                    target_list_name = new_list.name
                elif target_choice.isdigit() and 1 <= int(target_choice) <= len(other_lists):
                    target_list_id = other_lists[int(target_choice) - 1].id
                    target_list_name = other_lists[int(target_choice) - 1].name
                else:
                    print("❌ Invalid selection.")
                    input("Press Enter to continue...")
                    return

                # Move the task
                try:
                    self.manager.move_task_to_list(
                        self.current_list_id,
                        task.id,
                        target_list_id
                    )
                    print(f"\n✅ Task '{task.title}' moved to '{target_list_name}'!")
                    # Switch to the new list
                    self.current_list_id = target_list_id
                except ValueError as e:
                    print(f"\n❌ Error: {e}")

                input("Press Enter to continue...")
                self.task_management_menu()
            else:
                print("❌ Invalid selection.")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a number.")
            input("Press Enter to continue...")

    def filter_tasks(self) -> None:
        """Filter tasks by status."""
        print("\n🔍 Filter Tasks")
        print("-" * 70)

        options = {
            "1": "Show TODO tasks",
            "2": "Show IN_PROGRESS tasks",
            "3": "Show COMPLETED tasks",
            "4": "Show ALL tasks",
        }

        self.print_menu(options)
        choice = self.get_input("Select filter: ")

        status_map = {
            "1": TaskStatus.TODO,
            "2": TaskStatus.IN_PROGRESS,
            "3": TaskStatus.COMPLETED,
        }

        if choice in status_map:
            tasks = self.manager.get_tasks(self.current_list_id, status=status_map[choice])
            status_name = status_map[choice].value.upper()
        elif choice == "4":
            tasks = self.manager.get_tasks(self.current_list_id)
            status_name = "ALL"
        else:
            print("❌ Invalid option.")
            input("Press Enter to continue...")
            return

        if not tasks:
            print(f"\n📭 No {status_name} tasks found.")
        else:
            print(f"\n📋 {status_name} Tasks:")
            print("-" * 70)
            for i, task in enumerate(tasks, 1):
                priority_icon = "🔴" if task.priority == Priority.HIGH else (
                    "🟡" if task.priority == Priority.MEDIUM else "🟢"
                )
                print(f"  {i}. [{priority_icon}] {task.title}")

        input("\nPress Enter to continue...")
        self.task_management_menu()

    def search_menu(self) -> None:
        """Search menu."""
        self.clear_screen()
        self.print_header("🔍 Search Tasks")

        print("Search in: (1) Title  (2) Description  (3) Tags")
        search_choice = self.get_input("Select search field [1]: ").strip() or "1"

        search_map = {"1": "title", "2": "description", "3": "tags"}
        search_in = search_map.get(search_choice, "title")

        query = self.get_input("Enter search term: ")

        if not query:
            print("❌ Search query cannot be empty.")
            input("Press Enter to continue...")
            self.show_main_menu()
            return

        results = self.manager.search_tasks_across_lists(query, search_in=search_in)

        if not results:
            print(f"\n📭 No tasks found matching '{query}'")
        else:
            print(f"\n🔍 Search Results for '{query}' (in {search_in}):")
            print("-" * 70)
            for task_list, task in results:
                print(f"  📌 {task_list.name}: {task.title}")
                if task.description:
                    print(f"     📄 {task.description}")

        input("\nPress Enter to continue...")
        self.show_main_menu()

    def view_statistics(self) -> None:
        """View statistics."""
        self.clear_screen()
        self.print_header("📊 Statistics")

        stats = self.manager.get_statistics()

        print("\n📈 Overall Statistics:")
        print("-" * 70)
        print(f"  📂 Total Lists: {stats['total_lists']}")
        print(f"  📋 Total Tasks: {stats['total_tasks']}")
        print(f"  ✓ Completed: {stats['completed_tasks']}")
        print(f"  → In Progress: {stats['in_progress_tasks']}")
        print(f"  ○ To Do: {stats['todo_tasks']}")
        print(f"  📈 Completion: {stats['completion_percentage']}%")

        print("\n📋 Per-List Breakdown:")
        print("-" * 70)
        for task_list in self.manager.get_lists():
            tasks = self.manager.get_tasks(task_list.id)
            completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
            in_progress = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
            todo = sum(1 for t in tasks if t.status == TaskStatus.TODO)

            print(f"\n  {task_list.name}:")
            print(f"    ✓ Completed: {completed}")
            print(f"    → In Progress: {in_progress}")
            print(f"    ○ To Do: {todo}")
            print(f"    Total: {len(tasks)}")

        input("\nPress Enter to continue...")
        self.show_main_menu()

    def settings_menu(self) -> None:
        """Settings menu."""
        self.clear_screen()
        self.print_header("⚙️  Settings")

        options = {
            "1": "Save data (manual)",
            "2": "Clear all data",
            "3": "Back to main menu",
        }

        self.print_menu(options)
        choice = self.get_input("Select option: ")

        if choice == "1":
            self.manager.save()
            print("\n✅ Data saved!")
            input("Press Enter to continue...")
            self.settings_menu()
        elif choice == "2":
            confirm = self.get_input("Delete ALL data? (yes/no): ").lower()
            if confirm == "yes":
                self.manager.clear()
                print("\n✅ All data cleared!")
                self.current_list_id = None
            input("Press Enter to continue...")
            self.settings_menu()
        elif choice == "3":
            self.show_main_menu()
        else:
            print("❌ Invalid option.")
            input("Press Enter to continue...")
            self.settings_menu()

    def exit_app(self) -> None:
        """Exit the application."""
        self.clear_screen()
        confirm = self.get_input(
            "Save changes before exiting? (yes/no/cancel) [yes]: "
        ).lower()

        if confirm in ("yes", ""):
            self.manager.save()
            print("\n✅ Data saved!")
        elif confirm == "cancel":
            self.show_main_menu()
            return

        self.clear_screen()
        print("\n" + "=" * 70)
        print("  👋 Thank you for using To-Do List Manager!")
        print("=" * 70 + "\n")
        self.running = False

    def run(self) -> None:
        """Run the CLI application."""
        while self.running:
            self.show_main_menu()


def main() -> None:
    """Main entry point."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()
