"""Manual testing script to validate the Todo application."""

import sys
sys.path.insert(0, '.')

from src.infrastructure.memory_storage import MemoryStorage
from src.application.use_cases import AddTaskUseCase, ViewTasksUseCase, MarkCompleteUseCase
from src.domain.exceptions import EmptyDescriptionError, TaskNotFoundError

def test_basic_functionality():
    """Test basic add, view, and mark complete functionality."""
    print("Testing Todo Application...")

    # Setup
    storage = MemoryStorage()
    add_task = AddTaskUseCase(storage)
    view_tasks = ViewTasksUseCase(storage)
    mark_complete = MarkCompleteUseCase(storage)

    # Test 1: Add tasks
    print("\n1. Testing add task...")
    task1_id = add_task.execute("Buy groceries")
    task2_id = add_task.execute("Call mom")
    task3_id = add_task.execute("Finish report")
    print(f"[OK] Added 3 tasks (IDs: {task1_id}, {task2_id}, {task3_id})")

    # Test 2: View tasks
    print("\n2. Testing view tasks...")
    tasks = view_tasks.execute()
    assert len(tasks) == 3
    print(f"[OK] Found {len(tasks)} tasks")
    for task in tasks:
        status = "Complete" if task.is_complete else "Incomplete"
        print(f"   [{task.id}] {task.description} - {status}")

    # Test 3: Mark complete
    print("\n3. Testing mark complete...")
    mark_complete.execute(task1_id)
    tasks = view_tasks.execute()
    assert tasks[0].is_complete == True
    print(f"[OK] Task {task1_id} marked as complete")

    # Test 4: Empty description error
    print("\n4. Testing empty description validation...")
    try:
        add_task.execute("")
        print("[FAIL] Should have raised EmptyDescriptionError")
        return False
    except EmptyDescriptionError:
        print("[OK] Empty description correctly rejected")

    # Test 5: Task not found error
    print("\n5. Testing task not found error...")
    try:
        mark_complete.execute(999)
        print("[FAIL] Should have raised TaskNotFoundError")
        return False
    except TaskNotFoundError:
        print("[OK] Invalid task ID correctly rejected")

    print("\n[SUCCESS] All tests passed!")
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
