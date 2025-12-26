# Tasks: Phase I - In-Memory Todo Console

**Input**: Design documents from `specs/001-phase-i-in-memory/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), data-model.md (complete), contracts/ (complete)

**Tests**: Constitutional requirement (Principle V: Test-First Development) - tests MUST be written BEFORE implementation

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (per plan.md Section "Project Structure")

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure (src/, tests/, specs/, docs/)
- [ ] T002 Create pyproject.toml with project metadata and tool configurations (per quickstart.md)
- [ ] T003 [P] Create .python-version file with "3.11" content
- [ ] T004 [P] Create README.md with user-facing documentation (per quickstart.md)
- [ ] T005 [P] Create .gitignore for Python project (__pycache__/, .venv/, .pytest_cache/, .mypy_cache/, .coverage, htmlcov/)

**Checkpoint**: Project structure ready for code

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Domain Layer Foundation

- [ ] T006 Create src/__init__.py (empty init file for package)
- [ ] T007 Create src/domain/__init__.py (empty init file)
- [ ] T008 [P] Create src/domain/exceptions.py with custom exceptions (TaskNotFoundError, EmptyDescriptionError) per research.md Decision 3
- [ ] T009 Create tests/__init__.py (empty init file)
- [ ] T010 Create tests/unit/__init__.py (empty init file)

### Application Layer Foundation

- [ ] T011 Create src/application/__init__.py (empty init file)
- [ ] T012 Create src/application/storage.py with TaskStorage abstract interface (per plan.md Section "Clean Architecture")

### Infrastructure Layer Foundation

- [ ] T013 Create src/infrastructure/__init__.py (empty init file)

### Interface Layer Foundation

- [ ] T014 Create src/interface/__init__.py (empty init file)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks and view their task list

**Independent Test**: Launch app, add tasks, view list - delivers basic task tracker value

**Spec Reference**: spec.md lines 10-24 (User Story 1)
**Plan Reference**: plan.md Section "Clean Architecture" - Domain → Application → Infrastructure → Interface

### Tests for User Story 1 (MUST write FIRST per Constitutional Principle V)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T015 [P] [US1] Unit test for Task entity creation in tests/unit/test_task.py (test valid task, test empty description raises exception per data-model.md)
- [ ] T016 [P] [US1] Unit test for Task entity validation in tests/unit/test_task.py (test whitespace-only description, test special characters allowed)
- [ ] T017 [P] [US1] Unit test for MemoryStorage.save() in tests/unit/test_memory_storage.py (test ID generation, test task retrieval)
- [ ] T018 [P] [US1] Unit test for MemoryStorage.find_all() in tests/unit/test_memory_storage.py (test empty list, test multiple tasks)
- [ ] T019 [P] [US1] Unit test for AddTaskUseCase in tests/unit/test_use_cases.py (test successful add, test empty description error)
- [ ] T020 [P] [US1] Unit test for ViewTasksUseCase in tests/unit/test_use_cases.py (test empty list, test task display format)
- [ ] T021 [US1] Integration test for add and view flow in tests/integration/test_add_view_tasks.py (test spec acceptance scenarios 1-4)
- [ ] T022 [US1] Contract test for CLI menu display in tests/contract/test_cli_menu.py (test menu structure per contracts/cli-menu.md)
- [ ] T023 [US1] Contract test for "Add Task" operation in tests/contract/test_cli_menu.py (test input prompts, success messages, error messages)
- [ ] T024 [US1] Contract test for "View Tasks" operation in tests/contract/test_cli_menu.py (test task display format, empty list message)

### Implementation for User Story 1

**Domain Layer** (innermost - no dependencies):

- [ ] T025 [P] [US1] Implement Task entity in src/domain/task.py (dataclass with id, description, is_complete; __post_init__ validation per data-model.md)
- [ ] T026 [P] [US1] Implement Task.create() factory method in src/domain/task.py (validates description, returns Task instance)

**Infrastructure Layer** (implements storage):

- [ ] T027 [US1] Implement MemoryStorage class in src/infrastructure/memory_storage.py (dict storage, ID counter per research.md Decision 1-2)
- [ ] T028 [US1] Implement MemoryStorage.save(task) in src/infrastructure/memory_storage.py (assign ID, store in dict, return ID)
- [ ] T029 [US1] Implement MemoryStorage.find_all() in src/infrastructure/memory_storage.py (return list of all tasks sorted by ID)

**Application Layer** (use cases):

- [ ] T030 [US1] Implement AddTaskUseCase class in src/application/use_cases.py (takes storage, description; creates task, saves, returns ID)
- [ ] T031 [US1] Implement ViewTasksUseCase class in src/application/use_cases.py (takes storage; retrieves all tasks, formats for display)

**Interface Layer** (CLI):

- [ ] T032 [US1] Implement CLI.display_menu() in src/interface/cli.py (display 7 menu options per contracts/cli-menu.md)
- [ ] T033 [US1] Implement CLI.get_user_choice() in src/interface/cli.py (prompt for choice 1-7, validate numeric input)
- [ ] T034 [US1] Implement CLI.handle_add_task() in src/interface/cli.py (prompt for description, call use case, display success/error message)
- [ ] T035 [US1] Implement CLI.handle_view_tasks() in src/interface/cli.py (call use case, display tasks in format `[ID] Description - Status`)
- [ ] T036 [US1] Implement CLI.display_error() in src/interface/cli.py (display error with ✗ symbol per contracts/cli-menu.md)
- [ ] T037 [US1] Implement CLI.wait_for_keypress() in src/interface/cli.py (prompt "[Press Enter to continue...]")
- [ ] T038 [US1] Implement main application loop in src/interface/main.py (create storage, create CLI, run menu loop until quit)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can add and view tasks.

---

## Phase 4: User Story 2 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Enable users to track task completion status

**Independent Test**: Add tasks, mark complete, view updated status, toggle back to incomplete

**Spec Reference**: spec.md lines 27-41 (User Story 2)
**Plan Reference**: data-model.md Section "State Transitions"

### Tests for User Story 2 (MUST write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T039 [P] [US2] Unit test for MemoryStorage.find_by_id() in tests/unit/test_memory_storage.py (test valid ID, test invalid ID returns None)
- [ ] T040 [P] [US2] Unit test for MemoryStorage.update() in tests/unit/test_memory_storage.py (test task update, test ID not found raises exception)
- [ ] T041 [P] [US2] Unit test for MarkCompleteUseCase in tests/unit/test_use_cases.py (test mark complete, test idempotency, test invalid ID)
- [ ] T042 [P] [US2] Unit test for MarkIncompleteUseCase in tests/unit/test_use_cases.py (test mark incomplete, test idempotency, test invalid ID)
- [ ] T043 [US2] Integration test for mark complete/incomplete flow in tests/integration/test_mark_complete.py (test spec acceptance scenarios 1-4)
- [ ] T044 [US2] Contract test for "Mark Complete" operation in tests/contract/test_cli_menu.py (test input prompts, success messages, error messages)
- [ ] T045 [US2] Contract test for "Mark Incomplete" operation in tests/contract/test_cli_menu.py (test input prompts, success messages, error messages)

### Implementation for User Story 2

**Infrastructure Layer**:

- [ ] T046 [US2] Implement MemoryStorage.find_by_id(task_id) in src/infrastructure/memory_storage.py (return task or None)
- [ ] T047 [US2] Implement MemoryStorage.update(task) in src/infrastructure/memory_storage.py (update task in dict, raise TaskNotFoundError if not exists)

**Application Layer**:

- [ ] T048 [US2] Implement MarkCompleteUseCase class in src/application/use_cases.py (find task, set is_complete=True, update storage)
- [ ] T049 [US2] Implement MarkIncompleteUseCase class in src/application/use_cases.py (find task, set is_complete=False, update storage)

**Interface Layer**:

- [ ] T050 [US2] Implement CLI.get_task_id() in src/interface/cli.py (prompt for ID, validate numeric, return int or display error)
- [ ] T051 [US2] Implement CLI.handle_mark_complete() in src/interface/cli.py (get ID, call use case, display success/error)
- [ ] T052 [US2] Implement CLI.handle_mark_incomplete() in src/interface/cli.py (get ID, call use case, display success/error)
- [ ] T053 [US2] Update main loop in src/interface/main.py (add menu options 5 and 6 routing)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can add, view, and track task completion.

---

## Phase 5: User Story 3 - Update Task Description (Priority: P3)

**Goal**: Enable users to update task descriptions without deleting and re-adding

**Independent Test**: Add task, update description, verify change in list

**Spec Reference**: spec.md lines 44-56 (User Story 3)
**Plan Reference**: data-model.md Section "Task Update" validation rules

### Tests for User Story 3 (MUST write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T054 [P] [US3] Unit test for UpdateTaskUseCase in tests/unit/test_use_cases.py (test successful update, test empty description error, test invalid ID error)
- [ ] T055 [US3] Integration test for update task flow in tests/integration/test_update_task.py (test spec acceptance scenarios 1-3)
- [ ] T056 [US3] Contract test for "Update Task" operation in tests/contract/test_cli_menu.py (test input prompts, success messages, error messages)

### Implementation for User Story 3

**Application Layer**:

- [ ] T057 [US3] Implement UpdateTaskUseCase class in src/application/use_cases.py (find task, validate new description, update description, save)

**Interface Layer**:

- [ ] T058 [US3] Implement CLI.handle_update_task() in src/interface/cli.py (get ID, get new description, call use case, display success/error)
- [ ] T059 [US3] Update main loop in src/interface/main.py (add menu option 3 routing)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently. Users can modify task details.

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable users to remove unwanted tasks

**Independent Test**: Add tasks, delete specific task, verify removal from list

**Spec Reference**: spec.md lines 60-74 (User Story 4)
**Plan Reference**: data-model.md Section "Task Deletion" validation rules

### Tests for User Story 4 (MUST write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T060 [P] [US4] Unit test for MemoryStorage.delete(task_id) in tests/unit/test_memory_storage.py (test successful delete, test invalid ID raises exception, test ID not reused)
- [ ] T061 [P] [US4] Unit test for DeleteTaskUseCase in tests/unit/test_use_cases.py (test successful delete, test invalid ID error, test empty list handling)
- [ ] T062 [US4] Integration test for delete task flow in tests/integration/test_delete_task.py (test spec acceptance scenarios 1-4)
- [ ] T063 [US4] Contract test for "Delete Task" operation in tests/contract/test_cli_menu.py (test input prompts, success messages, error messages)

### Implementation for User Story 4

**Infrastructure Layer**:

- [ ] T064 [US4] Implement MemoryStorage.delete(task_id) in src/infrastructure/memory_storage.py (remove from dict, raise TaskNotFoundError if not exists)

**Application Layer**:

- [ ] T065 [US4] Implement DeleteTaskUseCase class in src/application/use_cases.py (find task, delete from storage)

**Interface Layer**:

- [ ] T066 [US4] Implement CLI.handle_delete_task() in src/interface/cli.py (get ID, call use case, display success/error)
- [ ] T067 [US4] Update main loop in src/interface/main.py (add menu option 4 routing)

**Checkpoint**: All user stories should now be independently functional. Full CRUD operations available.

---

## Phase 7: Application Lifecycle & Error Handling

**Purpose**: Complete application startup, shutdown, and comprehensive error handling

**Spec Reference**: spec.md FR-014, FR-015 (Quit option, continuous running)
**Plan Reference**: contracts/cli-menu.md Section "7. Quit", research.md Decision 3 (error handling)

### Tests (MUST write FIRST)

- [ ] T068 [P] Contract test for "Quit" operation in tests/contract/test_cli_menu.py (test quit message, test data loss warning per contracts/cli-menu.md)
- [ ] T069 [P] Contract test for invalid menu choice in tests/contract/test_cli_menu.py (test error message, return to menu)
- [ ] T070 [P] Contract test for unexpected errors in tests/contract/test_cli_menu.py (test generic error message, graceful recovery)

### Implementation

- [ ] T071 Implement CLI.handle_quit() in src/interface/cli.py (display goodbye message with data loss warning, return False to exit loop)
- [ ] T072 Implement CLI.handle_invalid_choice() in src/interface/cli.py (display error message "Invalid choice. Please enter a number between 1 and 7.")
- [ ] T073 Update main loop in src/interface/main.py (add menu option 7 routing, add try-except for unexpected errors per research.md)
- [ ] T074 Add exception handling in CLI methods (catch domain exceptions, display user-friendly messages, return to menu)

**Checkpoint**: Application has complete lifecycle management and robust error handling.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final quality improvements, documentation, and validation

**Spec Reference**: Constitutional Quality Standards (80% test coverage, type hints, docstrings)
**Plan Reference**: plan.md Section "Quality Standards Compliance"

- [ ] T075 [P] Add comprehensive docstrings (Google style) to all classes and methods in src/domain/task.py
- [ ] T076 [P] Add comprehensive docstrings (Google style) to all classes and methods in src/application/use_cases.py
- [ ] T077 [P] Add comprehensive docstrings (Google style) to all classes and methods in src/infrastructure/memory_storage.py
- [ ] T078 [P] Add comprehensive docstrings (Google style) to all classes and methods in src/interface/cli.py
- [ ] T079 [P] Add type hints to all function signatures (mypy strict mode compliance)
- [ ] T080 Run black formatter on all source files (src/ and tests/)
- [ ] T081 Run ruff linter and fix all issues (src/ and tests/)
- [ ] T082 Run mypy type checker and fix all type errors (src/)
- [ ] T083 Run pytest with coverage and ensure >= 80% (per constitutional requirement)
- [ ] T084 Verify quickstart.md instructions by following setup steps
- [ ] T085 Manual test all user stories end-to-end (add, view, update, delete, mark, quit)
- [ ] T086 Test edge cases (long descriptions, special characters, rapid operations per spec.md Edge Cases)

**Checkpoint**: All quality gates pass, ready for production.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion (can run parallel to US1 if staffed)
- **User Story 3 (Phase 5)**: Depends on Foundational phase completion (can run parallel to US1/US2 if staffed)
- **User Story 4 (Phase 6)**: Depends on Foundational phase completion (can run parallel to US1/US2/US3 if staffed)
- **Lifecycle (Phase 7)**: Depends on at least User Story 1 being complete
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Technically independent but builds on US1 concepts
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US2 but requires US1 foundation
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent of US2/US3

### Within Each User Story

**Critical Path** (MUST be sequential):
1. **Tests FIRST** (Red phase) - Write failing tests based on acceptance criteria
2. **Verify tests FAIL** - Run tests, confirm they fail as expected
3. **Domain implementation** - Implement domain layer (entities, validation)
4. **Infrastructure implementation** - Implement storage (depends on domain entities)
5. **Application implementation** - Implement use cases (depends on domain + infrastructure)
6. **Interface implementation** - Implement CLI handlers (depends on use cases)
7. **Verify tests PASS** - Run tests, confirm they now pass
8. **Refactor** (optional) - Clean up while keeping tests green

### Parallel Opportunities

- **Phase 1 (Setup)**: All tasks (T001-T005) can run in parallel
- **Phase 2 (Foundational)**: All __init__.py creation tasks can run in parallel (T006-T014)
- **Within User Stories**: Test creation tasks marked [P] can run in parallel
- **Across User Stories**: Once Foundational complete, US1/US2/US3/US4 can be worked on in parallel by different developers
- **Phase 8 (Polish)**: Documentation tasks (T075-T078) can run in parallel

### Sequential Requirements

**MUST be done in order**:
1. Phase 1 → Phase 2 → User Stories (Phase 3-6)
2. Within each user story: Tests → Domain → Infrastructure → Application → Interface
3. User Story 1 MUST be complete before application is usable (MVP)
4. Phase 7 (Lifecycle) MUST come after at least one user story
5. Phase 8 (Polish) MUST be last

---

## Parallel Execution Example: User Story 1 Tests

```bash
# Launch all test creation tasks for User Story 1 together:
Task T015: "Unit test for Task entity creation"
Task T016: "Unit test for Task entity validation"
Task T017: "Unit test for MemoryStorage.save()"
Task T018: "Unit test for MemoryStorage.find_all()"
Task T019: "Unit test for AddTaskUseCase"
Task T020: "Unit test for ViewTasksUseCase"

# All can be written simultaneously by different developers
# Then verify all FAIL before starting implementation
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T014) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T015-T038)
4. Complete Phase 7: Basic Lifecycle (T071-T074 for Quit functionality)
5. **STOP and VALIDATE**: Test User Story 1 independently
6. Run manual tests, verify all acceptance scenarios pass
7. This delivers a usable MVP (add and view tasks)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → **Usable MVP!**
3. Add User Story 2 → Test independently → **Progress tracking added**
4. Add User Story 3 → Test independently → **Task editing added**
5. Add User Story 4 → Test independently → **Task deletion added**
6. Add Polish (Phase 8) → **Production ready**
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (T001-T014)
2. Once Foundational is done:
   - **Developer A**: User Story 1 (T015-T038) - MVP priority
   - **Developer B**: User Story 2 (T039-T053) - Can work in parallel
   - **Developer C**: User Story 3 (T054-T059) - Can work in parallel
   - **Developer D**: User Story 4 (T060-T067) - Can work in parallel
3. **Team synchronizes**: Integrate all user stories
4. **Team completes**: Lifecycle (T068-T074) and Polish (T075-T086) together

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] label**: Maps task to specific user story for traceability (US1, US2, US3, US4)
- **Tests FIRST**: Constitutional requirement (Principle V) - write failing tests before implementation
- **Each user story should be independently completable and testable**
- **Verify tests fail before implementing** (Red phase of Red-Green-Refactor)
- **Verify tests pass after implementing** (Green phase)
- **Commit after each task or logical group** (reference task ID in commit message)
- **Stop at any checkpoint to validate story independently**
- **Avoid**: Vague tasks, same-file conflicts, cross-story dependencies that break independence

---

## Constitutional Compliance Verification

This task list complies with Evolution of Todo Project Constitution v1.0.0:

- ✅ **Spec-Driven Development (Principle I)**: All tasks derived from approved spec.md, no new features
- ✅ **Agent Autonomy Boundaries (Principle II)**: Tasks describe specific implementation steps from plan.md
- ✅ **Refinement at Spec Level (Principle III)**: No code-level decisions in tasks, all architecture in plan.md
- ✅ **Phase Boundary Enforcement (Principle IV)**: Zero Phase II+ concepts, explicit "no databases, no web, no persistence"
- ✅ **Test-First Development (Principle V)**: Test tasks BEFORE implementation tasks, explicit "MUST write FIRST" notes
- ✅ **Clean Architecture (Principle VI)**: Tasks organized by layer (Domain → Infrastructure → Application → Interface)
- ✅ **Cloud-Native Patterns (Principle VII)**: Stateless design enforced in use case implementations
- ✅ **Technology Constraints**: Python 3.11+, standard library only, pytest for testing
- ✅ **Quality Standards**: Docstrings (T075-T078), type hints (T079), linting (T081), coverage (T083)

**Task Count**: 86 tasks covering all 15 functional requirements from spec.md
**Estimated Completion**: MVP (User Story 1) = ~30 tasks, Full Phase I = 86 tasks

**Status**: ✅ **Task List Complete** - Ready for test-first implementation
