# Phase 0: Research Findings - Phase I In-Memory Todo Console

**Date**: 2025-12-26
**Feature**: Phase I - In-Memory Todo Console
**Branch**: `001-phase-i-in-memory`

## Purpose

This document captures research findings and technical decisions made during the planning phase. All decisions align with the Phase I specification and constitutional requirements.

## Research Questions & Answers

### Q1: What is the optimal in-memory storage structure for Phase I?

**Research Focus**: Evaluate Python data structures for task storage with O(1) lookup by ID.

**Options Evaluated**:

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Dictionary `{id: Task}` | O(1) lookup, insertion, deletion; Natural key-value mapping | Slightly more memory than list | ✅ **Selected** |
| List `[Task]` | Simple, preserves insertion order | O(n) lookup by ID; Requires linear search | ❌ Rejected - Poor performance |
| dataclass with __slots__ | Memory efficient | Overkill for Phase I; No significant benefit | ❌ Rejected - Unnecessary complexity |
| OrderedDict | Maintains insertion order + O(1) lookup | Unnecessary (dict is ordered in Python 3.7+) | ❌ Rejected - Standard dict sufficient |

**Decision**: Python dictionary `{task_id: Task}` with separate integer counter

**Rationale**:
- Provides O(1) lookups matching performance requirements (<100ms operations)
- Natural mapping of ID to Task object
- Simple to implement with no external dependencies
- Supports all CRUD operations efficiently
- Standard Python dict maintains insertion order (Python 3.7+) if needed for display

**Implementation Pattern**:
```python
class MemoryStorage:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
```

---

### Q2: How should task IDs be generated?

**Research Focus**: ID generation strategy that meets spec requirement FR-003 (auto-incrementing starting from 1).

**Options Evaluated**:

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Integer counter (1, 2, 3...) | Simple, human-friendly, matches spec | IDs not reused after delete | ✅ **Selected** |
| UUID v4 | Globally unique, no collisions | Not human-friendly; Overkill for Phase I | ❌ Rejected - Over-engineering |
| Timestamp-based ID | Sortable by creation time | Not guaranteed unique; Unexpected format | ❌ Rejected - Doesn't match spec |
| Reuse deleted IDs | Maximizes ID space usage | Complex logic; Can confuse users | ❌ Rejected - Added complexity |

**Decision**: Simple integer counter starting at 1, incremented on each add

**Rationale**:
- Directly implements spec requirement FR-003: "unique, auto-incrementing integer ID starting from 1"
- Human-friendly (users can easily reference Task 1, Task 2, etc.)
- No external dependencies (no UUID library needed)
- Simplest possible implementation
- Acceptable that IDs are not reused (spec doesn't require reuse, typical session <100 tasks)

**Implementation Pattern**:
```python
def add_task(self, task: Task) -> int:
    task_id = self._next_id
    self._next_id += 1
    self._tasks[task_id] = task
    return task_id
```

---

### Q3: Where should input validation occur?

**Research Focus**: Determine validation responsibilities across layers to maintain clean architecture.

**Options Evaluated**:

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Domain validates business rules, CLI validates format | Proper separation of concerns; Domain reusable | Requires coordination between layers | ✅ **Selected** |
| All validation in CLI | Simple, one place | Violates clean architecture; Business logic in UI | ❌ Rejected - Architecture violation |
| All validation in domain | Business logic centralized | Couples domain to I/O concerns | ❌ Rejected - Tight coupling |
| Validation layer (separate) | Clear responsibility | Overkill for Phase I; Extra layer | ❌ Rejected - Unnecessary complexity |

**Decision**: Domain validates business rules, CLI validates input format

**Rationale**:
- Maintains constitutional clean architecture requirement (Principle VI)
- Domain layer validates business rules (e.g., "description cannot be empty" - FR-010)
- Interface layer validates I/O format (e.g., "ID must be numeric" - for user input)
- Enables domain layer reuse in future phases (Phase II web interface can reuse domain validation)
- Clear separation: domain knows nothing about CLI, CLI knows about domain contracts

**Validation Mapping**:

| Validation | Layer | Reason |
|------------|-------|--------|
| Description non-empty | Domain | Business rule (applies regardless of interface) |
| Description length | Domain | Business constraint (if any limits defined) |
| ID is numeric | CLI | Input format concern (only matters for text input) |
| ID exists in storage | Application (Use Case) | Business logic (query operation) |
| Menu choice 1-7 | CLI | Interface concern (menu structure) |

---

### Q4: What error handling strategy should be used?

**Research Focus**: Exception handling approach that supports clean architecture and user experience.

**Options Evaluated**:

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Custom exceptions + CLI catch-all | Clean separation; Graceful degradation | Requires exception hierarchy design | ✅ **Selected** |
| Return codes (success/failure) | Simple, explicit | Not Pythonic; Hard to propagate errors | ❌ Rejected - Not idiomatic Python |
| Let exceptions bubble | Minimal code | User sees stack traces; Poor UX | ❌ Rejected - Violates FR-011 (clear error messages) |
| Exception hierarchy (many types) | Fine-grained error handling | Overkill for Phase I | ❌ Rejected - Unnecessary complexity |

**Decision**: Custom domain exceptions + graceful CLI error display + return to menu

**Rationale**:
- Domain raises specific exceptions for business rule violations (e.g., `EmptyDescriptionError`)
- Use cases propagate exceptions (no handling at this layer)
- CLI catches all exceptions, displays user-friendly message (per FR-011), returns to menu
- User never sees stack traces (good UX per SC-006: "Error messages are clear and actionable")
- Supports constitutional requirement for observability (can log exceptions)

**Exception Strategy**:

| Exception | Layer | Trigger | User Message |
|-----------|-------|---------|--------------|
| `TaskNotFoundError` | Domain/Use Case | ID doesn't exist in storage | "Task ID not found. Please check the ID and try again." |
| `EmptyDescriptionError` | Domain | Description is empty/whitespace | "Task description cannot be empty. Please provide a description." |
| `InvalidInputError` | CLI | Non-numeric ID entered | "Invalid input format. Please enter a number." |
| Generic `Exception` | Any | Unexpected errors | "An unexpected error occurred. Returning to main menu." |

---

### Q5: What testing strategy should be employed?

**Research Focus**: Test organization and tooling that meets constitutional requirements (80% coverage, test-first development).

**Options Evaluated**:

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| pytest + fixtures + 3 test dirs | Standard Python practice; Constitutional requirement | Requires test organization | ✅ **Selected** |
| unittest (stdlib) | No external deps | Verbose; Less flexible than pytest | ❌ Rejected - pytest mandated by constitution |
| pytest (flat structure) | Simple | Hard to navigate; No clear organization | ❌ Rejected - Poor scalability |
| pytest + tox (multi-env) | Tests multiple Python versions | Overkill for Phase I | ❌ Rejected - Unnecessary for single-version target |

**Decision**: pytest with fixtures, three test directories (unit, integration, contract)

**Rationale**:
- pytest is constitutionally mandated technology
- Three-directory structure maps to constitutional test categories:
  - **Unit tests**: Domain layer (Task entity) + Application layer (use cases) + Infrastructure (storage)
  - **Integration tests**: End-to-end user stories (map directly to spec User Story 1-4)
  - **Contract tests**: CLI behavior (menu options, input/output formats)
- Fixtures enable test setup reuse (e.g., pre-populated task list)
- Supports 80% minimum coverage requirement
- Enables test-first development (write failing test, implement, verify pass)

**Test Organization**:
```
tests/
├── unit/                 # Fast, isolated tests
│   ├── test_task.py      # Task entity validation
│   ├── test_use_cases.py # Business logic
│   └── test_memory_storage.py  # Storage operations
├── integration/          # End-to-end user stories
│   ├── test_add_view_tasks.py  # User Story 1
│   ├── test_mark_complete.py   # User Story 2
│   ├── test_update_task.py     # User Story 3
│   └── test_delete_task.py     # User Story 4
└── contract/             # Interface behavior
    └── test_cli_menu.py  # Menu options, I/O formats
```

---

## Best Practices Research

### Python 3.11+ Features to Leverage

**Type Hints (PEP 604)**:
```python
# Use new union syntax (Python 3.10+)
def find_task(self, task_id: int) -> Task | None:
    return self._tasks.get(task_id)
```

**Error Messages (PEP 678)**:
```python
# Enhanced exception notes (Python 3.11+)
try:
    task = storage.get_task(task_id)
except TaskNotFoundError as e:
    e.add_note(f"Attempted to access task ID: {task_id}")
    raise
```

**Dataclasses for Entities**:
```python
# Immutable entity with validation
from dataclasses import dataclass

@dataclass(frozen=True)
class Task:
    id: int
    description: str
    is_complete: bool = False

    def __post_init__(self):
        if not self.description.strip():
            raise EmptyDescriptionError()
```

### Clean Architecture Patterns for Python

**Repository Pattern (Simplified)**:
```python
# Abstract interface in application layer
from abc import ABC, abstractmethod

class TaskStorage(ABC):
    @abstractmethod
    def save(self, task: Task) -> int:
        pass

    @abstractmethod
    def find_by_id(self, task_id: int) -> Task | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Task]:
        pass
```

**Use Case Pattern**:
```python
# Each user action is a use case
class AddTaskUseCase:
    def __init__(self, storage: TaskStorage):
        self._storage = storage

    def execute(self, description: str) -> int:
        task = Task.create(description)  # Domain factory method
        return self._storage.save(task)
```

### Console Application Patterns

**Menu Loop Pattern**:
```python
def run(self):
    while True:
        self.display_menu()
        choice = self.get_user_choice()

        if choice == '7':  # Quit
            break

        try:
            self.handle_choice(choice)
        except Exception as e:
            self.display_error(str(e))

        self.wait_for_keypress()
```

**Input Validation Pattern**:
```python
def get_task_id(self) -> int:
    while True:
        user_input = input("Enter task ID: ").strip()
        try:
            task_id = int(user_input)
            if task_id < 1:
                print("Task ID must be positive.")
                continue
            return task_id
        except ValueError:
            print("Invalid input format. Please enter a number.")
```

---

## Technology Stack Finalization

### Mandated Technologies (from Constitution)

- **Language**: Python 3.11+ ✅
- **Testing**: pytest with coverage ✅
- **Type Checking**: mypy (strict mode) ✅
- **Linting**: ruff ✅
- **Formatting**: black ✅

### Additional Standard Library Modules

- `dataclasses` - Entity definition
- `abc` - Abstract base classes for interfaces
- `logging` - Observability (per constitutional Principle VII)
- `typing` - Type hints

### Development Dependencies Only

```toml
[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
mypy = "^1.5.0"
ruff = "^0.0.285"
black = "^23.7.0"
```

**No runtime dependencies** - standard library only per spec constraints.

---

## Architecture Pattern Justification

### Why Clean Architecture for Phase I?

**Question**: Is clean architecture overkill for a simple console app?

**Answer**: No, for the following reasons:

1. **Constitutional Requirement**: Principle VI mandates clean architecture with layer separation
2. **Future-Proofing**: Phase II will add database; clean separation means domain layer reusable without changes
3. **Testability**: Domain logic testable without CLI or storage dependencies
4. **Simplicity**: For Phase I, "clean architecture" is just four Python files (task.py, use_cases.py, memory_storage.py, cli.py)
5. **Maintainability**: Clear responsibilities make bugs easier to isolate and fix

**Trade-off**: Slightly more code upfront vs. massive reduction in future refactoring (Phase II+ won't require domain rewrite).

---

## Performance Considerations

### Expected Performance Profile

| Operation | Time Complexity | Expected Time | Requirement Met? |
|-----------|-----------------|---------------|------------------|
| Add Task | O(1) | ~0.001s | ✅ Yes (<10s per SC-001) |
| View Tasks | O(n) where n=tasks | ~0.01s for 100 tasks | ✅ Yes (<1s per SC-002) |
| Mark Complete/Incomplete | O(1) | ~0.001s | ✅ Yes (<15s per SC-003) |
| Update Task | O(1) | ~0.001s | ✅ Yes (<15s per SC-004) |
| Delete Task | O(1) | ~0.001s | ✅ Yes (<15s per SC-004) |

**Memory Usage**: ~1KB per task (generous estimate) → 1MB for 1000 tasks → Well under 512MB constitutional constraint.

---

## Risk Analysis

### Identified Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Over-engineering for future phases | Wasted effort | Medium | Explicit phase boundary checks; No unused abstractions |
| Underestimating test time | Delayed delivery | Low | Test-first approach ensures tests part of definition of done |
| Type hint complexity | Development friction | Low | Start simple; Gradual typing acceptable for Phase I |
| Memory leak (tasks accumulate) | Performance degradation | Very Low | Python GC handles cleanup; Session-limited (spec says <1000 tasks) |

**High-Confidence Assessment**: All risks low; architecture decisions sound; constitutional compliance verified.

---

## Alternatives Not Pursued

### Why Not Use FastAPI for Phase I?

**Reasoning**: Constitution mandates FastAPI for "Framework" but Phase I is explicitly a **console application** with no API requirements. FastAPI would violate phase boundaries (introducing web concepts) and add unnecessary complexity. Phase II will introduce FastAPI when web interface is specified.

### Why Not Add Logging Immediately?

**Reasoning**: Logging infrastructure planned (per Principle VII: Observability) but detailed logging deferred to implementation phase. Plan includes logging module import and basic configuration; extensive logging added during implementation if time allows.

### Why Not Use Pydantic for Validation?

**Reasoning**: Pydantic adds external dependency (violates "standard library only" constraint). Python 3.11 dataclasses with `__post_init__` validation sufficient for Phase I. Phase II may introduce Pydantic when FastAPI is added (FastAPI includes Pydantic).

---

## Research Conclusion

All technical decisions support Phase I specification requirements and constitutional principles. No unresolved questions remain. Architecture is simple, testable, and evolution-ready.

**Status**: ✅ **Research Complete** - Ready for Phase 1 design artifacts.
