"""Constants, enums, and default values for the to-do library."""

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


class OrderingStrategy(Enum):
    """Strategies for ordering lists."""

    MANUAL = "manual"
    RECENTLY_MODIFIED = "recently_modified"
    ALPHABETICAL = "alphabetical"
    CREATION_ORDER = "creation_order"
    RECENTLY_ADDED_TASK = "recently_added_task"


# Default values
DEFAULT_PRIORITY = Priority.MEDIUM
DEFAULT_TASK_STATUS = TaskStatus.TODO
DEFAULT_ORDERING_STRATEGY = OrderingStrategy.MANUAL
MAX_TASK_NAME_LENGTH = 200
MAX_LIST_NAME_LENGTH = 100
