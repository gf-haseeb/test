# My-Todo-Library

A customizable, Python-based to-do list library that allows developers to build terminal-based to-do applications with multiple list support and flexible ordering strategies.

## Features

- ✅ Create, read, update, delete tasks
- ✅ Multiple lists with custom organization
- ✅ Manual and automatic list ordering
- ✅ Task properties: title, description, status, priority, due date, tags
- ✅ JSON file persistence
- ✅ Easy-to-extend architecture

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd my-todo-library

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements.txt
```

## Quick Start

```python
from my_todo_lib import TaskManager, Task, OrderingStrategy

# Initialize manager
manager = TaskManager()

# Create lists
work = manager.create_list("Work")
personal = manager.create_list("Personal")

# Add tasks
task1 = Task(title="Fix bug", priority="high")
manager.add_task_to_list(work.id, task1)

task2 = Task(title="Buy groceries", priority="low")
manager.add_task_to_list(personal.id, task2)

# Get all lists (auto-sorted by modification time)
manager.set_list_ordering(OrderingStrategy.RECENTLY_MODIFIED)
for task_list in manager.get_lists():
    print(f"📋 {task_list.name}")
```

## Documentation

- [API Documentation](docs/API.md)
- [Examples](docs/EXAMPLES.md)
- [Project Guidelines](PROJECT_GUIDELINES.md)

## License

MIT License

## Author

Created with ❤️ by the development team
