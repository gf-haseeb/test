# My-Todo-Library: Project Guidelines & Rules

---
applyTo: "**"
---

**Last Updated:** 5 November 2025  
**Project Status:** Planning Phase  
**Version:** 1.0

---

## Table of Contents
1. [Project Vision](#project-vision)
2. [Architecture Rules](#architecture-rules)
3. [Code Standards](#code-standards)
4. [Naming Conventions](#naming-conventions)
5. [File Organization](#file-organization)
6. [Documentation Standards](#documentation-standards)
7. [Development Workflow](#development-workflow)
8. [Feature Scope](#feature-scope)

---

## Project Vision

**Goal:** Create a highly customizable, Python-based to-do list library that allows developers to build terminal-based to-do applications with multiple list support and flexible ordering strategies.

**Target Users:** Python developers who want to build to-do applications without building everything from scratch.

**Not Included (Out of Scope):**
- Web UI / GUI interfaces
- Database systems (only local JSON file for now)
- Cloud synchronization
- Real-time collaboration
- Email notifications
- SQLite or any database backends (Phase 2+)

---

## Architecture Rules

### Core Principle: Modularity
- Each component must be **independent and reusable**
- Components should communicate through well-defined interfaces
- No circular dependencies between modules

### Layer Structure
```
┌─ Presentation Layer (Manager API)
│
├─ Core Layer (Task, TaskList, ListContainer)
│
├─ Storage Layer (Abstract + Implementations)
│
└─ Utilities Layer (Constants, Helpers)
```

### Key Components (Non-Negotiable)

| Component | Responsibility | Location |
|-----------|-----------------|----------|
| `Task` | Individual task representation | `core/task.py` |
| `TaskList` | Collection of tasks in a single list | `core/task_list.py` |
| `ListContainer` | Manager for multiple lists + ordering | `core/list_container.py` |
| `TaskManager` | Public API facade | `manager.py` |
| `Storage` (Abstract) | Base storage interface | `storage/base.py` |
| `JSONStorage` | Local JSON file persistence | `storage/json_storage.py` |
| `Constants` | Enums & constants | `core/constants.py` |
| `Ordering` | Ordering strategies | `core/ordering.py` |

### Design Patterns to Use
- **Factory Pattern** - Creating tasks, lists, storage backends
- **Strategy Pattern** - Different ordering strategies
- **Abstract Base Classes** - Storage backends
- **Dependency Injection** - Pass storage to manager

---

## Code Standards

### Python Version
- **Minimum:** Python 3.7
- **Target:** Python 3.10+
- Use type hints for all functions

### Type Hints (Mandatory)
```python
# ✅ GOOD
def add_task(self, task: Task) -> bool:
    """Add a task to the list."""
    pass

# ❌ BAD
def add_task(self, task):
    pass
```

### Docstrings (Google Format)
```python
def get_tasks(self, status: str = None) -> List[Task]:
    """Retrieve tasks from the list with optional filtering.
    
    Args:
        status: Optional status filter ('todo', 'in_progress', 'completed')
        
    Returns:
        List of Task objects matching the criteria
        
    Raises:
        ValueError: If status is invalid
        
    Example:
        >>> tasks = task_list.get_tasks(status='completed')
    """
    pass
```

### Code Style
- **Line Length:** 100 characters max
- **Indentation:** 4 spaces (no tabs)
- **Imports:** Organize as standard, third-party, local (alphabetical within groups)
- **Method Order:** `__init__`, public methods, private methods, properties
- **Comments:** Explain WHY, not WHAT

### Error Handling
```python
# ✅ GOOD - Specific exceptions
class TaskNotFoundError(Exception):
    """Raised when task ID doesn't exist."""
    pass

# ❌ BAD - Generic exceptions
raise Exception("Task not found")
```

### Class Structure Template
```python
class MyClass:
    """Brief description of the class."""
    
    def __init__(self, param1: str, param2: int):
        """Initialize the class."""
        self._param1 = param1
        self._param2 = param2
    
    def public_method(self) -> str:
        """Public method description."""
        pass
    
    def _private_method(self) -> None:
        """Private method (prefixed with _)."""
        pass
    
    @property
    def property_name(self) -> str:
        """Property description."""
        return self._param1
```

---

## Naming Conventions

### Files & Folders
- **Lowercase with underscores:** `task_list.py`, `json_storage.py`
- **Folders lowercase:** `core/`, `storage/`, `examples/`
- **Test files:** `test_*.py` (e.g., `test_task.py`)

### Classes
- **PascalCase:** `Task`, `TaskList`, `ListContainer`, `TaskManager`
- **Exception classes end with `Error`:** `TaskNotFoundError`, `InvalidListError`

### Variables & Functions
- **lowercase_with_underscores:** `task_id`, `created_at`, `get_tasks()`
- **Constants: ALL_CAPS:** `DEFAULT_PRIORITY`, `MAX_TASK_NAME_LENGTH`

### Private Members
- **Prefix with underscore:** `self._internal_list`, `_helper_function()`

### Enums
```python
from enum import Enum

class TaskStatus(Enum):
    """Task status enumeration."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

---

## File Organization

### Folder Structure (Non-Negotiable)
```
my-todo-library/
├── my_todo_lib/                  # Main package
│   ├── __init__.py              # Exports public API
│   ├── core/
│   │   ├── __init__.py
│   │   ├── task.py              # Task class only
│   │   ├── task_list.py         # TaskList class only
│   │   ├── list_container.py    # ListContainer class only
│   │   ├── constants.py         # All enums
│   │   └── ordering.py          # Ordering strategies
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── base.py              # Abstract Storage class
│   │   └── json_storage.py      # JSON file implementation (only backend)
│   └── manager.py               # TaskManager class
├── examples/                     # CLI examples
│   ├── simple_todo.py           # Basic usage
│   ├── multi_list_todo.py       # Multi-list usage
│   └── advanced_todo.py         # Advanced features
├── tests/
│   ├── __init__.py
│   ├── test_task.py
│   ├── test_task_list.py
│   ├── test_list_container.py
│   ├── test_manager.py
│   └── test_storage.py
├── docs/
│   ├── API.md                   # API documentation
│   ├── EXAMPLES.md              # Usage examples
│   └── CONTRIBUTING.md          # Contribution guide
├── setup.py
├── requirements.txt
├── README.md
├── .gitignore
├── PROJECT_GUIDELINES.md        # This file
└── CHANGELOG.md
```

### One Class Per File Rule
- **One main class per file** (e.g., `task.py` contains only `Task`)
- **Exception:** Related helper classes in same file if tightly coupled
- **Benefits:** Easier to find code, cleaner git history, better organization

---

## Documentation Standards

### README.md Must Include
- Project description
- Installation instructions
- Quick start example
- Features list
- License

### API Documentation (API.md)
- All public classes with descriptions
- All public methods with parameters
- Return types and exceptions
- Code examples for each major component

### Docstring Requirements
- Every public class must have a docstring
- Every public method must have a docstring
- Private methods should have brief comments
- Describe edge cases and error conditions

### Example Docstring Format
```python
def move_list(self, list_id: int, position: int) -> None:
    """Reorder a list to a new position.
    
    Only works when ordering strategy is MANUAL.
    
    Args:
        list_id: The ID of the list to move
        position: Target position (0-indexed)
        
    Returns:
        None
        
    Raises:
        ListNotFoundError: If list_id doesn't exist
        InvalidOperationError: If ordering is not MANUAL
        
    Example:
        >>> manager.move_list(list_id=1, position=2)
    """
    pass
```

---

## Development Workflow

### Phase 1: Core Implementation (Current)
1. ✅ Define architecture (DONE)
2. Set up project structure
3. Implement core classes (Task, TaskList, ListContainer)
4. Implement storage layer
5. Implement TaskManager

### Phase 2: Testing
6. Write unit tests for all components
7. Achieve 80%+ code coverage
8. Test edge cases

### Phase 3: Examples & Docs
9. Create example CLI applications
10. Write comprehensive documentation
11. Add usage examples

### Phase 4: Refinement (Future)
12. Performance optimization
13. Add optional features
14. Community feedback

### Before Each Implementation Session
- Review relevant section of these guidelines
- Check if design matches planned architecture
- Verify naming follows conventions
- Ensure documentation is included

### Git Commit Message Format
```
[COMPONENT] Brief description

Detailed explanation if needed.
- Bullet point for changes
- Another bullet point

Fixes: #issue_number
```

Example:
```
[core] Implement ListContainer ordering strategies

- Add OrderingStrategy enum
- Implement MANUAL ordering
- Implement RECENTLY_MODIFIED ordering
- Add list reordering methods

Fixes: #5
```

---

## Feature Scope

### Phase 1 (MVP - Must Have)
- ✅ Create, read, update, delete tasks
- ✅ Create, read, delete lists
- ✅ Task properties: title, description, status, priority, due_date, tags
- ✅ List properties: name, description, creation time
- ✅ Multiple lists support
- ✅ Manual list ordering (MANUAL strategy)
- ✅ Auto list ordering (RECENTLY_MODIFIED strategy)
- ✅ JSON file persistence
- ✅ Basic filtering and sorting

### Phase 2 (Nice to Have)
- Filter tasks by multiple criteria
- Task recurrence support
- Task statistics per list
- List duplication/templates
- Export to CSV
- Task history/undo

### Phase 3+ (Future - After MVP Stable)
- SQLite storage backend
- Advanced filtering (date ranges, complex queries)
- Task dependencies
- Priority inheritance
- Custom fields

### ❌ Out of Scope (Never)
- Web UI/GUI
- Cloud sync
- Multi-user collaboration
- Real-time updates
- Mobile apps

---

## Consistency Checklist

Before committing code, verify:

- [ ] Code follows naming conventions (files, classes, methods, variables)
- [ ] Type hints present on all functions
- [ ] Docstrings in Google format on all public items
- [ ] No circular imports
- [ ] One class per file rule followed
- [ ] Private members prefixed with `_`
- [ ] No generic exception handling
- [ ] Imports organized (std, third-party, local)
- [ ] Lines under 100 characters
- [ ] Tests written for new functionality
- [ ] Example updated or created
- [ ] Matches planned architecture
- [ ] Git commit message follows format
- [ ] README/API docs updated if needed

---

## Questions & Decisions Log

**Format:** Record any architectural decisions made here

| Decision | Details | Date |
|----------|---------|------|
| Multiple lists support | Implemented via ListContainer class | 2025-11-05 |
| Ordering strategies | Strategy pattern with enums | 2025-11-05 |
| Storage approach | Abstract base + JSON/SQLite implementations | 2025-11-05 |
| (Add new decisions here) | ... | ... |

---

## Contact & Updates

**Created by:** AI Assistant (GitHub Copilot)  
**Last Modified:** 2025-11-05  
**Guidelines Version:** 1.0

*Keep this document updated as the project evolves. Review before major implementation phases.*
