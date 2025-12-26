# CLI Menu Contract: Phase I - In-Memory Todo Console

**Date**: 2025-12-26
**Feature**: Phase I - In-Memory Todo Console
**Branch**: `001-phase-i-in-memory`

## Purpose

This document specifies the exact behavior of the command-line interface, including menu structure, input formats, output formats, and user interaction flow. This is a **contract** that implementation must follow precisely to meet user expectations from the specification.

---

## Menu Structure

### Main Menu Display

**Format**:
```
=== Todo List Application ===

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Quit

Enter your choice (1-7):
```

**Requirements**:
- Menu displayed after every operation (except Quit)
- Options numbered 1-7 in exactly this order
- Clear visual separation (=== headers)
- Prompt explicitly states valid range (1-7)

---

## User Interaction Flow

### Application Startup

**Sequence**:
1. Application launched via `python src/interface/main.py`
2. Main menu displayed immediately
3. Cursor positioned after prompt waiting for input

**No startup messages** (no "Welcome!", "Loading...", etc. - just the menu).

---

### Menu Selection

**Input Format**: Single integer 1-7

**Valid Inputs**: `1`, `2`, `3`, `4`, `5`, `6`, `7`

**Invalid Inputs**:
- Non-numeric (e.g., `"abc"`, `"one"`)
- Out of range (e.g., `0`, `8`, `99`)
- Empty input (user presses Enter without typing)
- Multiple numbers (e.g., `"1 2"`)

**Error Handling**:
```
Invalid choice. Please enter a number between 1 and 7.
[Return to main menu]
```

---

## Operation Contracts

### 1. Add Task

**User Flow**:
```
Enter your choice (1-7): 1

Enter task description: Buy groceries

✓ Task added successfully with ID 1.

[Press Enter to continue...]
[Main menu redisplays]
```

**Input Validation**:

| Input | Result | Message |
|-------|--------|---------|
| "Buy groceries" | ✓ Success | "✓ Task added successfully with ID 1." |
| "" (empty) | ✗ Error | "✗ Task description cannot be empty. Please provide a description." |
| "   " (whitespace) | ✗ Error | "✗ Task description cannot be empty. Please provide a description." |
| "Task with emoji 🎉" | ✓ Success | "✓ Task added successfully with ID 2." |

**Post-Condition**: User returns to main menu after pressing Enter.

---

### 2. View Tasks

**User Flow (with tasks)**:
```
Enter your choice (1-7): 2

=== Task List ===

[1] Buy groceries - Incomplete
[2] Call mom - Complete
[3] Finish report - Incomplete

[Press Enter to continue...]
[Main menu redisplays]
```

**Display Format**:
- Each task: `[ID] Description - Status`
- Status values: "Complete" or "Incomplete" (not "True"/"False")
- Tasks displayed in ID order (lowest to highest)
- Blank line between header and first task
- Blank line after last task

**User Flow (empty list)**:
```
Enter your choice (1-7): 2

=== Task List ===

No tasks found. Add a task to get started!

[Press Enter to continue...]
[Main menu redisplays]
```

**Post-Condition**: User returns to main menu after pressing Enter.

---

### 3. Update Task

**User Flow**:
```
Enter your choice (1-7): 3

Enter task ID to update: 1
Enter new description: Buy groceries and milk

✓ Task 1 updated successfully.

[Press Enter to continue...]
[Main menu redisplays]
```

**Input Validation**:

| Task ID Input | Description Input | Result | Message |
|---------------|-------------------|--------|---------|
| "1" (valid) | "New description" | ✓ Success | "✓ Task 1 updated successfully." |
| "999" (invalid) | N/A | ✗ Error | "✗ Task ID not found. Please check the ID and try again." |
| "abc" (non-numeric) | N/A | ✗ Error | "✗ Invalid input format. Please enter a number." |
| "1" (valid) | "" (empty) | ✗ Error | "✗ Task description cannot be empty. Please provide a description." |

**Post-Condition**: User returns to main menu after pressing Enter.

---

### 4. Delete Task

**User Flow**:
```
Enter your choice (1-7): 4

Enter task ID to delete: 2

✓ Task 2 deleted successfully.

[Press Enter to continue...]
[Main menu redisplays]
```

**Input Validation**:

| Task ID Input | Result | Message |
|---------------|--------|---------|
| "2" (valid) | ✓ Success | "✓ Task 2 deleted successfully." |
| "999" (invalid) | ✗ Error | "✗ Task ID not found. Please check the ID and try again." |
| "abc" (non-numeric) | ✗ Error | "✗ Invalid input format. Please enter a number." |

**Special Case (empty list)**:
```
Enter task ID to delete: 1

✗ Task ID not found. Please check the ID and try again.

[Press Enter to continue...]
[Main menu redisplays]
```

**Post-Condition**: User returns to main menu after pressing Enter. Deleted task ID never appears again (not reused).

---

### 5. Mark Task Complete

**User Flow**:
```
Enter your choice (1-7): 5

Enter task ID to mark complete: 1

✓ Task 1 marked as complete.

[Press Enter to continue...]
[Main menu redisplays]
```

**Input Validation**:

| Task ID Input | Task Current Status | Result | Message |
|---------------|---------------------|--------|---------|
| "1" (valid) | Incomplete | ✓ Success | "✓ Task 1 marked as complete." |
| "1" (valid) | Already Complete | ✓ Success (idempotent) | "✓ Task 1 marked as complete." |
| "999" (invalid) | N/A | ✗ Error | "✗ Task ID not found. Please check the ID and try again." |
| "abc" (non-numeric) | N/A | ✗ Error | "✗ Invalid input format. Please enter a number." |

**Idempotency**: Marking an already-complete task as complete succeeds (no error).

**Post-Condition**: User returns to main menu after pressing Enter.

---

### 6. Mark Task Incomplete

**User Flow**:
```
Enter your choice (1-7): 6

Enter task ID to mark incomplete: 1

✓ Task 1 marked as incomplete.

[Press Enter to continue...]
[Main menu redisplays]
```

**Input Validation**:

| Task ID Input | Task Current Status | Result | Message |
|---------------|---------------------|--------|---------|
| "1" (valid) | Complete | ✓ Success | "✓ Task 1 marked as incomplete." |
| "1" (valid) | Already Incomplete | ✓ Success (idempotent) | "✓ Task 1 marked as incomplete." |
| "999" (invalid) | N/A | ✗ Error | "✗ Task ID not found. Please check the ID and try again." |
| "abc" (non-numeric) | N/A | ✗ Error | "✗ Invalid input format. Please enter a number." |

**Idempotency**: Marking an already-incomplete task as incomplete succeeds (no error).

**Post-Condition**: User returns to main menu after pressing Enter.

---

### 7. Quit

**User Flow**:
```
Enter your choice (1-7): 7

Goodbye! Your tasks will not be saved.

[Application terminates]
```

**Post-Condition**: Application exits with status code 0 (success). No menu redisplays.

**Data Loss Warning**: Explicit message that data is not persisted (per Phase I in-memory requirement).

---

## Input Specifications

### Task Description Input

**Prompt**: `"Enter task description: "`

**Format**: Free-form text, single line

**Accepted Characters**: Any Unicode characters (letters, numbers, spaces, punctuation, emojis, etc.)

**Termination**: User presses Enter/Return

**Validation**:
- ✓ Non-empty after trimming: Accepted
- ✗ Empty or whitespace-only: Rejected with error

**Edge Cases**:

| Input | Accepted? | Notes |
|-------|-----------|-------|
| "Buy groceries" | ✓ Yes | Normal case |
| "  Buy groceries  " | ✓ Yes | Leading/trailing spaces preserved |
| "Task\nwith\nnewlines" | ✓ Yes | Newlines allowed (user can paste multi-line) |
| "" | ✗ No | Empty description error |
| "     " | ✗ No | Whitespace-only error |
| "x" * 1000 | ✓ Yes | Long descriptions allowed (edge case per spec) |

---

### Task ID Input

**Prompt**: Varies by operation:
- Update: `"Enter task ID to update: "`
- Delete: `"Enter task ID to delete: "`
- Mark Complete: `"Enter task ID to mark complete: "`
- Mark Incomplete: `"Enter task ID to mark incomplete: "`

**Format**: Integer >= 1

**Validation**:
- ✓ Numeric string convertible to positive integer: Accepted
- ✗ Non-numeric: Rejected with "Invalid input format"
- ✗ Numeric but ID doesn't exist: Rejected with "Task ID not found"

**Edge Cases**:

| Input | Validation Result | Message |
|-------|-------------------|---------|
| "1" | ✓ Pass format check | (Then check if exists) |
| "0" | ✓ Pass format check | (Then fail existence check - IDs start at 1) |
| "-5" | ✓ Pass format check | (Then fail existence check - negative IDs invalid) |
| "abc" | ✗ Fail format check | "✗ Invalid input format. Please enter a number." |
| "1.5" | ✗ Fail format check | "✗ Invalid input format. Please enter a number." |
| "1 2" | ✗ Fail format check | "✗ Invalid input format. Please enter a number." |

---

### Menu Choice Input

**Prompt**: `"Enter your choice (1-7): "`

**Format**: Integer 1-7

**Validation**:
- ✓ "1" through "7": Accepted, corresponding operation executed
- ✗ Other: Rejected with "Invalid choice"

---

## Output Specifications

### Success Messages

**Format**: `✓ [Action] [Details].`

**Examples**:
- `✓ Task added successfully with ID 1.`
- `✓ Task 5 updated successfully.`
- `✓ Task 3 deleted successfully.`
- `✓ Task 2 marked as complete.`
- `✓ Task 7 marked as incomplete.`

**Characteristics**:
- Start with ✓ symbol (checkmark)
- End with period
- Include relevant details (ID, action)
- Clear, affirmative language

---

### Error Messages

**Format**: `✗ [Problem description]. [Actionable guidance].`

**Examples**:
- `✗ Task ID not found. Please check the ID and try again.`
- `✗ Task description cannot be empty. Please provide a description.`
- `✗ Invalid input format. Please enter a number.`
- `✗ Invalid choice. Please enter a number between 1 and 7.`

**Characteristics**:
- Start with ✗ symbol (cross mark)
- Two sentences: Problem + Guidance
- End with period
- Never show stack traces or technical details

---

### Continuation Prompt

**Format**: `[Press Enter to continue...]`

**Behavior**:
- Displayed after every operation (except Quit)
- Waits for user to press Enter/Return
- After Enter pressed, clear screen (optional but recommended) and redisplay main menu

---

## Error Recovery

### Transient Errors

**Definition**: Errors that user can immediately correct (wrong ID, empty description, invalid format).

**Behavior**:
1. Display error message
2. Display continuation prompt
3. Return to main menu
4. User can retry operation with corrected input

**No Error**: User never "trapped" in error state; always returns to main menu.

---

### Unexpected Errors

**Definition**: Errors not anticipated by specification (e.g., system errors, bugs).

**Behavior**:
1. Display generic error message: `✗ An unexpected error occurred. Returning to main menu.`
2. Log error details to stderr (for debugging)
3. Return to main menu

**User Impact**: Minimal - operation fails but application continues running.

---

## Screen Layout Conventions

### Clear Separation

**Recommended**: Clear screen between operations for clean visual experience (optional, not required).

**Alternative**: Use blank lines (2-3) to visually separate menu from previous output.

---

### Consistent Formatting

**Headers**: Use `===` for section headers
- `=== Todo List Application ===`
- `=== Task List ===`

**Status Indicators**:
- Success: ✓ (checkmark)
- Error: ✗ (cross mark)
- Status values: "Complete" / "Incomplete" (capitalized)

**Prompts**: End with colon and space
- `Enter your choice (1-7): `
- `Enter task description: `

---

## Performance Requirements

### Response Time

| Operation | Maximum Time | Typical Time |
|-----------|--------------|--------------|
| Display menu | Instant | <10ms |
| Add task | <100ms | <10ms |
| View tasks (100 tasks) | <1000ms | <100ms |
| Update task | <100ms | <10ms |
| Delete task | <100ms | <10ms |
| Mark complete/incomplete | <100ms | <10ms |

**Rationale**: Constitutional requirement (Phase I: <100ms 95th percentile). Meets spec success criteria SC-001 through SC-004 (all operations <15 seconds user experience time including reading and typing).

---

## Accessibility Considerations

### Text-Only Interface

**Requirement**: Application must work in any standard terminal (no graphics, no colors required).

**Optional Enhancements** (not required for Phase I):
- ANSI color codes for success (green) / error (red)
- Bold text for headers
- Unicode box-drawing characters for better visuals

**Baseline**: Plain text must be fully functional.

---

### Screen Reader Compatibility

**Requirement**: All output must be readable by screen readers (text-based output only).

**Avoid**: ASCII art, fancy formatting that doesn't narrate well.

---

## Contract Verification

### Test Scenarios

Each acceptance scenario from the specification maps to specific CLI interactions:

**User Story 1 (Add and View Tasks)**:
1. Launch app → See menu
2. Choose "1" → Prompted for description
3. Enter "Buy groceries" → See success message with ID 1
4. Press Enter → Return to menu
5. Choose "2" → See task displayed `[1] Buy groceries - Incomplete`

**User Story 2 (Mark Complete/Incomplete)**:
1. Choose "5" → Prompted for task ID
2. Enter "1" → See success message
3. Choose "2" → See task displayed `[1] Buy groceries - Complete`
4. Choose "6" → Prompted for task ID
5. Enter "1" → See success message
6. Choose "2" → See task displayed `[1] Buy groceries - Incomplete`

**User Story 3 (Update Task)**:
1. Choose "3" → Prompted for task ID
2. Enter "1" → Prompted for new description
3. Enter "Buy whole milk" → See success message
4. Choose "2" → See updated task `[1] Buy whole milk - Incomplete`

**User Story 4 (Delete Task)**:
1. Choose "4" → Prompted for task ID
2. Enter "1" → See success message
3. Choose "2" → See "No tasks found"

---

## Constitutional Compliance

✅ **Clean Architecture (Principle VI)**:
- Contract defines interface layer behavior without exposing domain/application logic
- CLI is "outermost layer" with dependencies pointing inward

✅ **Phase Boundary Enforcement (Principle IV)**:
- No web/API concepts (pure console interface)
- No persistence indicators (explicit "will not be saved" message)
- No multi-user concepts

✅ **Test-First Development (Principle V)**:
- Contract tests verify menu structure, input handling, output format
- Integration tests verify end-to-end user stories against this contract

---

## Summary

The CLI contract defines a simple, text-based menu-driven interface for all Phase I operations. The interface prioritizes clarity (explicit prompts, clear messages), error handling (never crash, always return to menu), and performance (<100ms operations). All user stories from the specification are directly implementable through this contract.

**Status**: ✅ **CLI Contract Complete** - Ready for quickstart guide.
