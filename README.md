# Advanced Task Management Suite

A comprehensive, Python-based task management library with auto-save persistence, multi-list support, intelligent task ordering, and an interactive CLI. Perfect for building sophisticated terminal-based productivity applications.

## ✨ Features

- ✅ **Full CRUD Operations** - Create, read, update, delete tasks with validation
- ✅ **Multiple Lists** - Organize tasks across multiple custom lists
- ✅ **Flexible Ordering** - Manual and automatic task ordering (by priority, creation date, status)
- ✅ **Auto-Save Persistence** - Automatic JSON storage after every operation
- ✅ **Rich Task Properties** - Title, description, status, priority, due date, tags
- ✅ **Move Tasks Between Lists** - Seamlessly reorganize tasks across lists
- ✅ **Interactive CLI** - Full-featured terminal interface for daily use
- ✅ **Enterprise-Grade Testing** - 142 unit tests, 80%+ coverage, 100% pass rate
- ✅ **CI/CD Ready** - GitHub Actions workflow for multi-version Python testing (3.9, 3.10, 3.11)
- ✅ **Easy-to-Extend Architecture** - Clean design for custom implementations

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd advanced-task-manager

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements.txt
```

## 🚀 Quick Start - Interactive CLI (Recommended)

The fastest way to experience the library is through the interactive CLI:

```bash
# Run the interactive CLI
python examples/interactive_cli.py
```

**Features in Interactive CLI:**
- Create, edit, and delete tasks interactively
- Organize tasks across multiple lists
- Move tasks between lists with ease
- View tasks sorted by priority, creation date, or status
- Auto-save with every operation
- Intuitive menu-driven interface

**Example CLI Workflow:**
```
Main Menu
1. Create a new list
2. View all lists
3. Create a new task
4. View tasks in a list
5. Update task status
6. Move task to another list
7. Delete a task
8. Exit

Enter your choice: 1
Enter list name: Work Projects
✅ List created: Work Projects

Enter your choice: 3
Select list: 1. Work Projects
Enter task title: Implement new API endpoint
Enter task priority (1-5): 1
✅ Task created and auto-saved!
```

## 📖 Quick Start - Python API

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

# Move tasks between lists
manager.move_task_to_list(
    source_list_id=personal.id,
    task_id=task2.id,
    target_list_id=work.id
)

# Get all lists (auto-sorted by modification time)
manager.set_list_ordering(OrderingStrategy.RECENTLY_MODIFIED)
for task_list in manager.get_lists():
    print(f"📋 {task_list.name}")
```

## 📚 Documentation & Examples

### Core Documentation
- [API Documentation](API_DOCUMENTATION.md) - Complete API reference
- [Project Guidelines](PROJECT_GUIDELINES.md) - Architecture and coding standards
- [CI/CD Guide](CI_CD_GUIDE.md) - GitHub Actions pipeline documentation
- [Move Task Feature](MOVE_TASK_FEATURE.md) - Moving tasks between lists guide

### Example Scripts
The `examples/` directory contains working demonstrations:
- `interactive_cli.py` - Full-featured interactive terminal interface (recommended!)
- `simple_todo.py` - Basic usage example
- `ordering_demo.py` - Task ordering strategies
- `advanced_demo.py` - Advanced features showcase
- `cli_autosave_demo.py` - Auto-save verification
- `test_move_task_feature.py` - Move task feature integration test

## 🧪 Testing & Quality

```bash
# Run all 142 tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=my_todo_lib --cov-report=html

# Check code style
flake8 my_todo_lib/

# Auto-format code
black my_todo_lib/ tests/
```

**Project Metrics:**
- Tests: 142 (100% pass rate)
- Coverage: 85%+
- Python Versions: 3.9, 3.10, 3.11
- CI/CD: GitHub Actions (automatic on every push)

## 🏗️ Architecture

```
my_todo_lib/
├── core/              (8 core components)
│   ├── task.py        (Task model)
│   ├── task_list.py   (List container)
│   ├── list_container.py (All lists)
│   ├── constants.py   (Configuration)
│   └── ordering.py    (Sorting logic)
├── storage/           (Persistence layer)
│   ├── base_storage.py (Abstract interface)
│   └── json_storage.py (JSON implementation)
└── manager.py         (Main API orchestrator)
```

## 🔄 Auto-Save Persistence

Every operation automatically saves to `~/.my_todo_lib/tasks.json`:

```python
# Create task - auto-saved immediately
task = manager.create_task(list_id, "My Task")

# Update task - auto-saved immediately
manager.update_task(task.id, status="completed")

# Move task - auto-saved immediately
manager.move_task_to_list(source_id, task.id, target_id)

# No manual save() needed - it's automatic!
```

## 🎯 Use Cases

- **Personal Productivity** - Manage daily tasks and lists
- **Team Collaboration** - Organize project tasks
- **Learning Project** - Understand Python architecture and testing
- **CLI Applications** - Base for building task-based tools
- **Task Orchestration** - Programmatic task management

## 📊 Test Coverage

| Component | Tests | Status |
|-----------|-------|--------|
| Task | 27 | ✅ |
| TaskList | 33 | ✅ |
| ListContainer | 31 | ✅ |
| Storage | 17 | ✅ |
| Manager | 28 | ✅ |
| **Total** | **142** | **✅ 100%** |

## 🚀 CI/CD Pipeline

GitHub Actions automatically runs on every commit:
- Tests on Python 3.9, 3.10, 3.11
- Code quality checks (flake8, black, pylint)
- Coverage reporting
- Test summary and status

See [CI/CD Guide](CI_CD_GUIDE.md) for detailed information.

## 💡 Common Tasks

### Create and organize tasks
```python
manager = TaskManager()
work_list = manager.create_list("Work")
task = manager.create_task(work_list.id, "Complete project", priority=1)
```

### Move tasks between lists
```python
manager.move_task_to_list(
    source_list_id="list_001",
    task_id="task_001",
    target_list_id="list_002"
)
```

### Sort tasks by priority
```python
manager.set_task_ordering(OrderingStrategy.PRIORITY)
tasks = manager.get_all_tasks_across_lists()
```

## 🔧 Development Setup

```bash
# Clone and setup
git clone <repo-url>
cd advanced-task-manager
python3 -m venv venv
source venv/bin/activate
pip install -e .
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run interactive CLI
python examples/interactive_cli.py
```

## 📝 Contributing

This project follows strict code standards:
- PEP 8 compliance
- Type hints required
- Google-style docstrings
- 80%+ test coverage
- All tests passing

See `.github/copilot-instructions.md` for detailed guidelines.

## License

MIT License

## Author

Created with ❤️ by the development team
