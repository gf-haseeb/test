# 📚 To-Do List Library - Setup Guide

Welcome! This guide will help you get the to-do list library up and running in minutes.

## 📋 Table of Contents
- [Quick Start (5 minutes)](#quick-start)
- [Installation](#installation)
- [Core Concepts](#core-concepts)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### 1. Clone/Download the Library
```bash
# Navigate to the project directory
cd my-todo-lib
```

### 2. Create a Virtual Environment
```bash
# Python 3.7+
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Your First Script
```python
from my_todo_lib.manager import TaskManager

# Create manager (auto-saves to tasks.json)
manager = TaskManager()

# Create a list
my_list = manager.create_list("My Tasks")

# Add a task
task = manager.add_task_to_list(my_list.id, "Learn Python")

print(f"✅ Created task: {task.title}")
```

That's it! Your data is automatically saved to `tasks.json`.

---

## 📦 Installation

### Prerequisites
- **Python**: 3.7 or higher
- **pip**: Python package manager

### Step-by-Step Installation

#### 1. Extract/Clone the Project
```bash
git clone <repo-url>
cd my_todo_lib
```

#### 2. Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `pytest` - For running tests
- `pytest-cov` - For code coverage

#### 4. Verify Installation
```bash
# Run all tests
python3 -m pytest tests/ -v

# You should see: "136 passed"
```

---

## 💡 Core Concepts

### The Four Main Components

#### 1. **Task** - A single to-do item
```python
task = Task(
    title="Fix bug",
    description="Critical bug in database",
    priority=Priority.HIGH,
    status=TaskStatus.TODO,
    tags=["urgent", "backend"]
)
```

**Properties:**
- `id`: Auto-generated unique identifier
- `title`: Task name (required)
- `description`: Detailed info
- `status`: TODO, IN_PROGRESS, COMPLETED
- `priority`: LOW, MEDIUM, HIGH
- `tags`: List of labels
- `due_date`: Optional deadline

#### 2. **TaskList** - A collection of tasks
```python
task_list = TaskList(
    name="Work Projects",
    description="All work-related tasks"
)
task_list.add_task(task)
```

**Features:**
- Organize tasks into logical groups
- Filter tasks by status
- Sort tasks by priority/date
- Clear completed tasks

#### 3. **ListContainer** - Manages multiple lists
```python
from my_todo_lib.core.constants import OrderingStrategy

container = ListContainer(
    ordering_strategy=OrderingStrategy.ALPHABETICAL
)
list1 = container.create_list("Work")
list2 = container.create_list("Personal")
```

**Ordering Strategies:**
- `MANUAL`: Custom order (default)
- `ALPHABETICAL`: A-Z by name
- `CREATION_ORDER`: By creation date
- `RECENTLY_MODIFIED`: Recently updated first
- `RECENTLY_ADDED_TASK`: Lists with newest tasks first

#### 4. **TaskManager** - Main API (what you'll use)
```python
from my_todo_lib.manager import TaskManager

manager = TaskManager()  # Auto-saves to tasks.json

# Everything goes through the manager
manager.create_list("Shopping")
manager.add_task_to_list(list_id, "Buy milk")
manager.get_statistics()
```

---

## 🎯 Basic Usage

### Creating Lists and Tasks

```python
from my_todo_lib.manager import TaskManager
from my_todo_lib.core.constants import Priority, TaskStatus

manager = TaskManager()

# Create a list
work = manager.create_list("Work")

# Add tasks
task1 = manager.add_task_to_list(
    work.id,
    title="Complete project",
    description="Finish Q4 project",
    priority=Priority.HIGH
)

task2 = manager.add_task_to_list(
    work.id,
    title="Code review",
    priority=Priority.MEDIUM,
    tags=["review", "team"]
)

print(f"Created {work.task_count} tasks")
```

### Retrieving Data

```python
# Get all lists
all_lists = manager.get_lists()

# Get specific list
my_list = manager.get_list(list_id)

# Get tasks from a list
tasks = manager.get_tasks(list_id)

# Get specific task
task = manager.get_task(list_id, task_id)
```

### Updating Tasks

```python
# Update status
manager.update_task(
    list_id,
    task_id,
    status=TaskStatus.IN_PROGRESS
)

# Update priority
manager.update_task(
    list_id,
    task_id,
    priority=Priority.HIGH
)

# Update multiple fields
manager.update_task(
    list_id,
    task_id,
    status=TaskStatus.COMPLETED,
    priority=Priority.MEDIUM
)
```

### Deleting Items

```python
# Delete a task
manager.delete_task(list_id, task_id)

# Delete a list
manager.delete_list(list_id)
```

---

## 🔥 Advanced Features

### Search Across Lists

```python
# Search by title
results = manager.search_tasks_across_lists("bug")

# Search by description
results = manager.search_tasks_across_lists(
    "database",
    search_in="description"
)

# Search by tags
results = manager.search_tasks_across_lists(
    "urgent",
    search_in="tags"
)

# Results are tuples: (TaskList, Task)
for task_list, task in results:
    print(f"{task_list.name}: {task.title}")
```

### List Ordering

```python
from my_todo_lib.core.constants import OrderingStrategy

# Set ordering strategy
manager.set_list_ordering(OrderingStrategy.ALPHABETICAL)

# Get ordered lists
ordered = manager.get_lists()

# Manual reordering
manager.move_list(list_id, new_position)
```

### Statistics and Analytics

```python
stats = manager.get_statistics()

print(f"Total Lists: {stats['total_lists']}")
print(f"Total Tasks: {stats['total_tasks']}")
print(f"Completed: {stats['completed_tasks']}")
print(f"In Progress: {stats['in_progress_tasks']}")
print(f"To Do: {stats['todo_tasks']}")
print(f"Completion %: {stats['completion_percentage']}%")
```

### Data Persistence

```python
# Automatic save on every mutation (create, update, delete)
manager.create_list("Auto-saved")

# Manual save
manager.save()

# Load from storage
manager.load()

# Clear all data
manager.clear()
```

### Custom Storage

```python
from my_todo_lib.storage.json_storage import JSONStorage

# Use custom file path
storage = JSONStorage("my_tasks.json")
manager = TaskManager(storage=storage)
```

---

## 📂 Examples

The library includes three runnable examples:

### 1. Simple To-Do CLI
```bash
python3 examples/simple_todo.py
```
**Demonstrates:**
- Creating lists and tasks
- Adding descriptions and priorities
- Marking tasks complete
- Basic statistics
- Search functionality

### 2. List Ordering Demo
```bash
python3 examples/ordering_demo.py
```
**Demonstrates:**
- All 5 ordering strategies
- Moving lists to new positions
- Persistence and reloading
- Strategy comparison

### 3. Advanced Features
```bash
python3 examples/advanced_demo.py
```
**Demonstrates:**
- Complex search scenarios
- Priority filtering
- Tag-based search
- Per-list statistics
- Task updates and deletion

---

## 🔌 API Reference

### TaskManager Methods

#### List Management
```python
# Create
list = manager.create_list(name, description="")

# Retrieve
lists = manager.get_lists()
list = manager.get_list(list_id)

# Update
manager.rename_list(list_id, new_name)
manager.set_list_ordering(OrderingStrategy)
manager.move_list(list_id, new_position)  # MANUAL only

# Delete
manager.delete_list(list_id)  # Raises ValueError if not found
```

#### Task Management
```python
# Create
task = manager.add_task_to_list(
    list_id,
    title,
    description="",
    status=TaskStatus.TODO,
    priority=Priority.MEDIUM,
    due_date=None,
    tags=None
)

# Retrieve
tasks = manager.get_tasks(list_id)
task = manager.get_task(list_id, task_id)

# Update
manager.update_task(
    list_id,
    task_id,
    status=TaskStatus.IN_PROGRESS,
    priority=Priority.HIGH,
    # ... other fields
)

# Delete
manager.delete_task(list_id, task_id)
```

#### Search & Analytics
```python
# Search
results = manager.search_tasks_across_lists(
    query,
    search_in="title"  # or "description", "tags"
)

# Statistics
stats = manager.get_statistics()
```

#### Persistence
```python
manager.save()    # Manual save
manager.load()    # Load from storage
manager.clear()   # Clear all data
```

---

## 🧪 Testing

### Run All Tests
```bash
python3 -m pytest tests/ -v
```

### Run Specific Test File
```bash
python3 -m pytest tests/test_manager.py -v
```

### Run with Coverage
```bash
python3 -m pytest tests/ --cov=my_todo_lib --cov-report=html
```

**Test Coverage:**
- ✅ 136 total tests
- ✅ Task class (27 tests)
- ✅ TaskList class (33 tests)
- ✅ ListContainer class (31 tests)
- ✅ JSONStorage (17 tests)
- ✅ TaskManager (28 tests)

---

## ❓ Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'my_todo_lib'`
**Solution:**
```bash
# Make sure you're in the project directory
cd /path/to/my_todo_lib

# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run from project root
python3 -c "from my_todo_lib.manager import TaskManager"
```

### Issue: Data not saving
**Solution:**
```python
# Ensure you call save() or it's auto-saved on mutations
manager = TaskManager()
manager.create_list("Test")  # Auto-saves

# Or manually save
manager.save()

# Verify file exists
import os
print(os.path.exists("tasks.json"))  # Should be True
```

### Issue: Tests failing
**Solution:**
```bash
# Ensure all dependencies installed
pip install -r requirements.txt

# Run specific test for details
python3 -m pytest tests/test_manager.py::TestTaskManagerListOperations::test_create_list -v
```

### Issue: Can't find examples
**Solution:**
```bash
# Examples are in the examples/ directory
python3 examples/simple_todo.py

# Make sure you're in the project root
cd /path/to/my_todo_lib
```

---

## 📝 Tips & Best Practices

### 1. Always Use Manager
```python
# ✅ Good - Use TaskManager
from my_todo_lib.manager import TaskManager
manager = TaskManager()

# ❌ Avoid - Direct class usage (no auto-save)
from my_todo_lib.core.task import Task
task = Task(...)  # No auto-save!
```

### 2. Check for None Returns
```python
# ✅ Good
task = manager.get_task(list_id, task_id)
if task:
    print(task.title)

# ❌ Avoid
print(manager.get_task(list_id, task_id).title)  # Crashes if None
```

### 3. Use Constants
```python
# ✅ Good
from my_todo_lib.core.constants import Priority, TaskStatus
manager.add_task_to_list(list_id, "Task", priority=Priority.HIGH)

# ❌ Avoid
manager.add_task_to_list(list_id, "Task", priority="high")  # String
```

### 4. Handle Errors
```python
# ✅ Good
try:
    manager.delete_list(999)
except ValueError as e:
    print(f"Error: {e}")

# ❌ Avoid
manager.delete_list(999)  # Crashes if not found
```

### 5. Search is Case-Insensitive
```python
# All these find the same task with title "Buy Milk"
manager.search_tasks_across_lists("buy")
manager.search_tasks_across_lists("BUY")
manager.search_tasks_across_lists("Buy")
```

---

## 🎓 Learning Path

**New to the library?** Follow this path:

1. ✅ Read this guide (5 min)
2. ✅ Run `examples/simple_todo.py` (2 min)
3. ✅ Create your first task in Python REPL (5 min)
4. ✅ Run `examples/advanced_demo.py` (3 min)
5. ✅ Review `examples/ordering_demo.py` code (5 min)
6. ✅ Build your first app! 🚀

---

## 📞 Support

### Documentation Files
- `README.md` - Project overview
- `PROJECT_GUIDELINES.md` - Code standards
- `COMPLIANCE_CHECKLIST.md` - Architecture docs

### Test Examples
Run tests to see usage patterns:
```bash
grep -r "def test_" tests/ | head -20
```

### Code Examples
- `examples/simple_todo.py` - Basic usage
- `examples/ordering_demo.py` - Ordering strategies
- `examples/advanced_demo.py` - Advanced features

---

## 🎉 You're Ready!

You now have everything you need to build awesome to-do list applications. Start building! 🚀

For questions or issues, refer back to the relevant section or check the test files for more examples.

**Happy coding!** ✨
