# Data Model: Phase I - In-Memory Todo Console

**Date**: 2025-12-26
**Feature**: Phase I - In-Memory Todo Console
**Branch**: `001-phase-i-in-memory`

## Purpose

This document defines all entities, their attributes, relationships, validation rules, and state transitions for Phase I. This is a **business model**, not an implementation specification—it describes WHAT the data represents, not HOW it is stored.

---

## Entities

### Task

Represents a single todo item that a user wants to track and complete.

**Attributes**:

| Attribute | Type | Required | Mutable | Default | Description |
|-----------|------|----------|---------|---------|-------------|
| `id` | Integer | Yes | No | Auto-generated | Unique identifier for the task, starting from 1 and incrementing |
| `description` | String | Yes | Yes | None | Text describing what needs to be done |
| `is_complete` | Boolean | Yes | Yes | `False` | Completion status: `True` if complete, `False` if incomplete |

**Attribute Details**:

- **id**:
  - **Purpose**: Uniquely identify tasks for operations (update, delete, mark complete)
  - **Generation**: Auto-assigned by system on task creation, sequential starting from 1
  - **Constraints**: Must be positive integer >= 1, never reused even after deletion
  - **Immutability**: Cannot be changed after creation (users never set or modify IDs)

- **description**:
  - **Purpose**: Human-readable text explaining the task
  - **Constraints**:
    - MUST NOT be empty (zero-length string not allowed)
    - MUST NOT be whitespace-only (e.g., "   " not allowed)
    - No maximum length enforced (spec assumes <500 chars typical, edge cases up to 1000+ chars acceptable)
  - **Mutability**: Can be updated by user via Update Task operation
  - **Special Characters**: All Unicode characters allowed (emojis, quotes, newlines, etc.)

- **is_complete**:
  - **Purpose**: Track whether the task has been finished
  - **Values**: Boolean `True` (Complete) or `False` (Incomplete)
  - **Display**: Shown to user as "Complete" or "Incomplete" (not "True"/"False")
  - **Mutability**: Toggled by user via Mark Complete / Mark Incomplete operations
  - **Default**: New tasks start as `False` (Incomplete)

---

## Validation Rules

### Task Creation

**Pre-conditions**:
1. Description provided by user
2. Description is non-empty after trimming whitespace

**Validation**:
- ✅ **PASS**: `description.strip()` returns non-empty string
- ❌ **FAIL**: `description.strip()` returns empty string → Raise `EmptyDescriptionError`

**Post-conditions**:
1. Task created with auto-generated ID
2. Task created with `is_complete = False`
3. Description stored exactly as provided (no trimming or modification)

**Example Valid Inputs**:
- "Buy groceries"
- "  Call mom  " (leading/trailing spaces preserved)
- "Task with emoji 🎉"
- "Multi\nline\ntask" (newlines allowed)

**Example Invalid Inputs**:
- "" (empty string) → Error: "Task description cannot be empty"
- "   " (whitespace only) → Error: "Task description cannot be empty"

---

### Task Update

**Pre-conditions**:
1. Task ID provided by user
2. Task with given ID exists in system
3. New description provided by user
4. New description is non-empty after trimming whitespace

**Validation**:
- ✅ **PASS**: Task exists AND `new_description.strip()` returns non-empty string
- ❌ **FAIL (ID)**: Task doesn't exist → Raise `TaskNotFoundError`
- ❌ **FAIL (Description)**: `new_description.strip()` returns empty → Raise `EmptyDescriptionError`

**Post-conditions**:
1. Task description updated to new value
2. Task ID unchanged
3. Task completion status unchanged

---

### Task Completion Toggle

**Pre-conditions**:
1. Task ID provided by user
2. Task with given ID exists in system

**Validation**:
- ✅ **PASS**: Task exists
- ❌ **FAIL**: Task doesn't exist → Raise `TaskNotFoundError`

**Post-conditions**:
- **Mark Complete**: `is_complete` set to `True`
- **Mark Incomplete**: `is_complete` set to `False`
- Task ID and description unchanged

---

### Task Deletion

**Pre-conditions**:
1. Task ID provided by user
2. Task with given ID exists in system

**Validation**:
- ✅ **PASS**: Task exists
- ❌ **FAIL**: Task doesn't exist → Raise `TaskNotFoundError`

**Post-conditions**:
1. Task removed from system
2. Task ID not reused for future tasks
3. Other tasks unaffected (IDs remain unchanged)

---

## State Transitions

### Task Lifecycle

```
┌──────────┐
│  [User]  │
└────┬─────┘
     │ Add Task
     │ (with description)
     ▼
┌─────────────────────┐
│   Task Created      │
│   is_complete=False │  ◄─── Initial State
│   (Incomplete)      │
└──────┬──────────────┘
       │
       │ Mark Complete
       ▼
┌─────────────────────┐
│  is_complete=True   │
│   (Complete)        │
└──────┬──────────────┘
       │
       │ Mark Incomplete
       ▼
┌─────────────────────┐
│  is_complete=False  │
│   (Incomplete)      │  ◄─── Can toggle repeatedly
└──────┬──────────────┘
       │
       │ Delete Task
       ▼
┌─────────────────────┐
│   Task Removed      │  ◄─── Terminal State
│   (No longer exists)│
└─────────────────────┘
```

**State Descriptions**:

1. **Created (Incomplete)**: Task exists, not yet completed
   - User can: View, Update description, Mark complete, Delete
   - Transition to: Complete (via Mark Complete) or Removed (via Delete)

2. **Complete**: Task exists, marked as finished
   - User can: View, Update description, Mark incomplete, Delete
   - Transition to: Incomplete (via Mark Incomplete) or Removed (via Delete)

3. **Removed**: Task no longer exists in system
   - Terminal state (no transitions out)
   - ID permanently retired (not reused)

**State Transition Rules**:
- ✅ Incomplete ↔ Complete (bidirectional, unlimited toggles)
- ✅ Any state → Removed (deletion always possible)
- ❌ Removed → Any state (deleted tasks cannot be restored in Phase I)

---

## Business Rules

### Rule 1: Unique Task IDs

**Rule**: Each task MUST have a unique ID that no other task (past or present) has used.

**Rationale**: Users reference tasks by ID for operations. Reusing IDs would confuse users ("I deleted Task 5, why is there a new Task 5?").

**Implementation Constraint**: ID counter only increments, never resets or reuses deleted IDs.

---

### Rule 2: Non-Empty Descriptions

**Rule**: Task descriptions MUST contain at least one non-whitespace character.

**Rationale**: Empty tasks provide no value to users and create confusion ("What is Task 7 supposed to be?").

**Implementation Constraint**: Validate on creation and update; reject empty/whitespace-only strings.

---

### Rule 3: Default Incomplete Status

**Rule**: Newly created tasks MUST start in the Incomplete state.

**Rationale**: Users add tasks to track work that needs to be done. Completed tasks don't need tracking.

**Implementation Constraint**: `is_complete` defaults to `False` on creation; no user option to create pre-completed tasks.

---

### Rule 4: ID Immutability

**Rule**: Task IDs MUST NOT change after creation.

**Rationale**: Users reference tasks by ID in subsequent operations. Changing IDs breaks user mental model and invalidates references.

**Implementation Constraint**: ID assigned once at creation, never modified.

---

### Rule 5: Description Mutability

**Rule**: Task descriptions MUST be updatable without affecting task ID or completion status.

**Rationale**: Users make typos or need to refine task details. Forcing delete-and-recreate loses completion status and changes ID.

**Implementation Constraint**: Update operation modifies only description field.

---

## Data Integrity Constraints

### Constraint 1: ID Uniqueness

**Constraint**: No two tasks (active or deleted) may share the same ID.

**Verification**: ID generation uses monotonically increasing counter; no manual ID assignment.

**Violation Impact**: System behavior undefined; user operations unpredictable.

---

### Constraint 2: ID Continuity

**Constraint**: ID sequence may have gaps (e.g., 1, 2, 5, 8) but must always increase.

**Verification**: Next ID always greater than all previous IDs.

**Violation Impact**: Potential ID collision; user confusion.

---

### Constraint 3: Reference Integrity

**Constraint**: All task references (by ID) must resolve to exactly one task or fail with `TaskNotFoundError`.

**Verification**: Storage lookup returns task or None; no ambiguous cases.

**Violation Impact**: Operations fail unexpectedly or affect wrong task.

---

## Entity Relationships

### Phase I (In-Memory)

**No relationships** - Phase I has a single entity (Task) with no relationships to other entities.

**Rationale**: Phase I scope excludes multi-user, categories, tags, etc. Each task is independent.

**Future Phases**: Relationships will be added:
- Phase II: Task → User (ownership)
- Phase III: Task → Agent (assignment)
- Phase IV: Task → Project (organization)

**Design Note**: Single-entity model simplifies Phase I implementation. Future relationships added without breaking Task entity definition (only new attributes added, existing attributes unchanged per constitutional backward compatibility).

---

## Data Volume & Scale

### Expected Data Characteristics

**Typical Session**:
- Tasks: 5-20
- Longest description: ~100 characters
- Session duration: 10-30 minutes

**Edge Case Session** (per spec assumptions):
- Tasks: Up to 1000
- Longest description: ~1000 characters
- Session duration: Several hours

**Memory Estimation**:
- Task object: ~200 bytes (ID: 8 bytes, description: ~100 bytes avg, is_complete: 1 byte, overhead: ~90 bytes)
- 100 tasks: ~20 KB
- 1000 tasks: ~200 KB
- Well under 512MB constitutional memory constraint

**Performance Impact**:
- Storage: O(1) lookup, O(1) insert, O(1) delete → No performance degradation with scale
- Display: O(n) iteration for "View Tasks" → Linear, but n ≤ 1000 → <1 second per SC-002

---

## Error Scenarios

### Missing Task

**Scenario**: User provides task ID that doesn't exist (never created, or previously deleted).

**Business Rule Violated**: Reference Integrity Constraint

**System Response**: Raise `TaskNotFoundError` with message "Task ID not found. Please check the ID and try again."

**User Impact**: Operation aborted, user returns to menu, can retry with correct ID.

---

### Empty Description

**Scenario**: User provides empty string or whitespace-only string as task description.

**Business Rule Violated**: Non-Empty Descriptions Rule

**System Response**: Raise `EmptyDescriptionError` with message "Task description cannot be empty. Please provide a description."

**User Impact**: Task not created/updated, user returns to menu, can retry with valid description.

---

### Invalid ID Format

**Scenario**: User enters non-numeric input when task ID expected (e.g., "abc" instead of "5").

**Business Rule Violated**: None (input format error, not business rule)

**System Response**: CLI layer catches input error, displays "Invalid input format. Please enter a number."

**User Impact**: Operation not attempted, user prompted to re-enter ID.

---

## Compliance Verification

### Constitutional Alignment

✅ **Clean Architecture (Principle VI)**:
- Entity defined without implementation details (no storage mechanism mentioned)
- Validation rules belong to domain layer
- State transitions are business logic, not technical flow

✅ **Phase Boundary Enforcement (Principle IV)**:
- No Phase II+ concepts (users, authentication, persistence, categories)
- No foreign keys or relationship tables
- No "reserved for future use" attributes

✅ **Technology Agnostic**:
- No Python-specific details in entity definition
- Could be implemented in any language with integers, strings, booleans

---

## Summary

Phase I data model consists of a single **Task** entity with three attributes (ID, description, completion status). The model is simple, validates essential business rules (non-empty descriptions, unique IDs), and supports all Phase I user stories without future-phase contamination.

**Status**: ✅ **Data Model Complete** - Ready for contract definitions.
