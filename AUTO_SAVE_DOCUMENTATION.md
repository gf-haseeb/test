# Auto-Save Feature Documentation

## Overview

The **interactive CLI application** automatically saves all list and task changes to a JSON file without requiring any manual action. Every modification is immediately persisted to disk.

## How Auto-Save Works

The auto-save functionality is built into the `TaskManager` class, which is used by the interactive CLI. Here's what happens:

### 1. **Automatic Save on Every Change**

Every method that modifies lists or tasks automatically calls `self.save()` to persist changes:

| Operation | Auto-Save | JSON Updated |
|-----------|-----------|--------------|
| Create list | ✅ Yes | ✅ Yes |
| Rename list | ✅ Yes | ✅ Yes |
| Delete list | ✅ Yes | ✅ Yes |
| Change list ordering | ✅ Yes | ✅ Yes |
| Move list | ✅ Yes | ✅ Yes |
| Add task | ✅ Yes | ✅ Yes |
| Update task | ✅ Yes | ✅ Yes |
| Delete task | ✅ Yes | ✅ Yes |
| Mark task complete | ✅ Yes | ✅ Yes |

### 2. **JSON File Structure**

The data is saved in a `tasks.json` file (or any name you specify) with the following structure:

```json
{
  "ordering_strategy": "manual",
  "created_at": "2025-11-05T15:33:40.659534",
  "modified_at": "2025-11-05T15:33:40.671305",
  "lists": [
    {
      "id": 1,
      "name": "Work Tasks",
      "description": "My work items",
      "created_at": "2025-11-05T15:33:40.659555",
      "modified_at": "2025-11-05T15:33:40.670881",
      "tasks": [
        {
          "id": 1,
          "title": "Complete project",
          "description": "Finish the project deadline",
          "status": "completed",
          "priority": "high",
          "due_date": null,
          "tags": ["urgent", "work"],
          "created_at": "2025-11-05T15:33:40.659890",
          "modified_at": "2025-11-05T15:33:40.669493"
        }
      ]
    }
  ],
  "metadata": {
    "1": {
      "custom_index": 0,
      "created_at": "2025-11-05T15:33:40.659557"
    }
  }
}
```

### 3. **Data Persistence**

- **Created At**: Timestamp when list/task was created
- **Modified At**: Timestamp when list/task was last modified
- **Ordering Strategy**: Current ordering strategy for lists
- **Metadata**: Internal data for list ordering
- **All changes preserved**: Every modification is immediately saved

## Running the Interactive CLI with Auto-Save

When you run the interactive CLI:

```bash
python3 examples/interactive_cli.py
```

All your actions are automatically saved:

1. **Create a list** → Immediately saved to `tasks.json`
2. **Add a task** → Immediately saved to `tasks.json`
3. **Update task status** → Immediately saved to `tasks.json`
4. **Mark complete** → Immediately saved to `tasks.json`
5. **Change list order** → Immediately saved to `tasks.json`
6. **Delete items** → Immediately saved to `tasks.json`

### Exit and Resume

Even if you close the application:
- All data is safely stored in `tasks.json`
- On next run, all lists and tasks are automatically loaded
- Your progress is never lost

## Testing Auto-Save

To see auto-save in action, run the test script:

```bash
python3 examples/test_autosave.py
```

This will:
- Create lists and tasks
- Verify each operation updates the JSON file
- Display the final JSON content
- Confirm all data is persisted correctly

## Example: Manual Save (Optional)

If needed, you can also manually save from the CLI settings menu:

```
Main Menu → Settings → Save data (manual)
```

However, this is **not required** since auto-save handles all changes automatically.

## Data Recovery

If you want to reload your data into a fresh CLI session:

1. The `tasks.json` file is automatically loaded on startup
2. All your lists and tasks are restored
3. No manual import/export needed

## Performance Note

- Auto-save happens **immediately** after each operation
- JSON serialization is **very fast** (< 1ms typically)
- No noticeable delay in the CLI user experience

## File Location

By default, `tasks.json` is created in the same directory where you run the CLI. You can specify a different location by modifying the `interactive_cli.py`:

```python
# Change this line to use a different file path
self.manager = TaskManager(storage=JSONStorage("path/to/tasks.json"))
```

## Summary

✅ **Auto-save is built in and working**
✅ **JSON file updated on every change**
✅ **Data persists between sessions**
✅ **No manual save required** (but optional manual save available)
✅ **All operations immediately persisted**
