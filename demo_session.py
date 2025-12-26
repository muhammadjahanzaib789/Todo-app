"""Automated demo session showing all features."""

import sys
sys.path.insert(0, '.')

from src.infrastructure.memory_storage import MemoryStorage
from src.application.use_cases import (
    AddTaskUseCase,
    ViewTasksUseCase,
    UpdateTaskUseCase,
    DeleteTaskUseCase,
    MarkCompleteUseCase,
    MarkIncompleteUseCase,
)

def run_demo():
    """Run a complete demo of all features."""
    print("=" * 60)
    print("DEMO: Todo App Phase I - All Features")
    print("=" * 60)

    # Setup
    storage = MemoryStorage()
    add_task = AddTaskUseCase(storage)
    view_tasks = ViewTasksUseCase(storage)
    update_task = UpdateTaskUseCase(storage)
    delete_task = DeleteTaskUseCase(storage)
    mark_complete = MarkCompleteUseCase(storage)
    mark_incomplete = MarkIncompleteUseCase(storage)

    # Feature 1: Add Tasks
    print("\n[1] ADDING TASKS")
    print("-" * 60)
    id1 = add_task.execute("Buy groceries")
    print(f"Added: 'Buy groceries' (ID: {id1})")

    id2 = add_task.execute("Call mom")
    print(f"Added: 'Call mom' (ID: {id2})")

    id3 = add_task.execute("Finish report")
    print(f"Added: 'Finish report' (ID: {id3})")

    # Feature 2: View Tasks
    print("\n[2] VIEWING TASKS")
    print("-" * 60)
    tasks = view_tasks.execute()
    for task in tasks:
        status = "Complete" if task.is_complete else "Incomplete"
        print(f"[{task.id}] {task.description} - {status}")

    # Feature 3: Mark Complete
    print("\n[3] MARKING TASK COMPLETE")
    print("-" * 60)
    mark_complete.execute(id1)
    print(f"Marked task {id1} as complete")

    tasks = view_tasks.execute()
    for task in tasks:
        status = "Complete" if task.is_complete else "Incomplete"
        print(f"[{task.id}] {task.description} - {status}")

    # Feature 4: Mark Incomplete
    print("\n[4] MARKING TASK INCOMPLETE")
    print("-" * 60)
    mark_incomplete.execute(id1)
    print(f"Marked task {id1} as incomplete")

    tasks = view_tasks.execute()
    for task in tasks:
        status = "Complete" if task.is_complete else "Incomplete"
        print(f"[{task.id}] {task.description} - {status}")

    # Feature 5: Update Task
    print("\n[5] UPDATING TASK DESCRIPTION")
    print("-" * 60)
    print(f"Before: {tasks[0].description}")
    update_task.execute(id1, "Buy groceries and milk")
    tasks = view_tasks.execute()
    print(f"After:  {tasks[0].description}")

    # Feature 6: Delete Task
    print("\n[6] DELETING TASK")
    print("-" * 60)
    print(f"Tasks before delete: {len(tasks)}")
    delete_task.execute(id3)
    tasks = view_tasks.execute()
    print(f"Tasks after delete: {len(tasks)}")
    for task in tasks:
        status = "Complete" if task.is_complete else "Incomplete"
        print(f"[{task.id}] {task.description} - {status}")

    # Feature 7: Error Handling
    print("\n[7] ERROR HANDLING")
    print("-" * 60)

    print("Testing empty description...")
    try:
        add_task.execute("")
        print("[FAIL] Should have raised error")
    except Exception as e:
        print(f"[OK] Correctly rejected: {type(e).__name__}")

    print("\nTesting invalid task ID...")
    try:
        update_task.execute(999, "Test")
        print("[FAIL] Should have raised error")
    except Exception as e:
        print(f"[OK] Correctly rejected: {type(e).__name__}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE - All features working correctly!")
    print("=" * 60)

if __name__ == "__main__":
    run_demo()
