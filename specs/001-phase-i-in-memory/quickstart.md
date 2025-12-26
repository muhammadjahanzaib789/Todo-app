# Quick Start Guide: Phase I - In-Memory Todo Console

**Date**: 2025-12-26
**Feature**: Phase I - In-Memory Todo Console
**Branch**: `001-phase-i-in-memory`

## Purpose

This guide helps developers set up their development environment and begin implementing Phase I of the Evolution of Todo project. Follow these steps in order for a smooth onboarding experience.

---

## Prerequisites

### Required Software

- **Python 3.11 or higher** - [Download here](https://www.python.org/downloads/)
  - Verify: `python --version` (should show 3.11.x or higher)
  - Note: Use `python3` on systems where `python` points to Python 2.x

- **pip** - Python package installer (included with Python 3.11+)
  - Verify: `pip --version`

- **Git** - Version control system
  - Verify: `git --version`

### Recommended Software

- **Virtual environment support** - Built into Python 3.11 (venv module)
- **Code editor** - VS Code, PyCharm, or any text editor
- **Terminal** - Command Prompt (Windows), Terminal (macOS/Linux), or Git Bash

---

## Environment Setup

### Step 1: Clone Repository

```bash
# If repository already cloned, skip this step
git clone <repository-url>
cd todo-app

# Check out the Phase I branch
git checkout 001-phase-i-in-memory
```

---

### Step 2: Create Virtual Environment

**Windows (Command Prompt)**:
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Windows (PowerShell)**:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Verification**: Your terminal prompt should now show `(.venv)` prefix.

---

### Step 3: Install Development Dependencies

```bash
pip install --upgrade pip

# Install testing and quality tools
pip install pytest pytest-cov mypy ruff black
```

**Expected Output**:
```
Successfully installed pytest-X.X.X pytest-cov-X.X.X mypy-X.X.X ruff-X.X.X black-X.X.X
```

**Verification**:
```bash
pytest --version  # Should show pytest 7.4.0 or higher
mypy --version    # Should show mypy 1.5.0 or higher
ruff --version    # Should show ruff 0.0.285 or higher
black --version   # Should show black 23.7.0 or higher
```

---

### Step 4: Verify Project Structure

```bash
# Check that directory structure exists
ls -R  # Unix/macOS
dir /s  # Windows
```

**Expected Structure** (will be created during implementation):
```
todo-app/
├── src/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── interface/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── specs/
│   └── 001-phase-i-in-memory/
│       ├── spec.md
│       ├── plan.md
│       ├── data-model.md
│       ├── research.md
│       ├── quickstart.md (this file)
│       └── contracts/
│           └── cli-menu.md
├── pyproject.toml (to be created)
├── README.md (to be created)
└── .python-version (to be created)
```

---

## Configuration Files

### Create pyproject.toml

**Purpose**: Define project metadata, dependencies, and tool configurations.

**File**: `pyproject.toml` (in project root)

**Content**:
```toml
[project]
name = "todo-app-phase-i"
version = "1.0.0"
description = "Phase I: In-Memory Todo Console Application"
requires-python = ">=3.11"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.5.0",
    "ruff>=0.0.285",
    "black>=23.7.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--verbose",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "N", "W", "UP"]

[tool.black]
line-length = 100
target-version = ["py311"]
```

---

### Create .python-version

**Purpose**: Pin Python version for consistency across development environments.

**File**: `.python-version` (in project root)

**Content**:
```
3.11
```

---

### Create README.md

**Purpose**: User-facing documentation for running the application.

**File**: `README.md` (in project root)

**Content**:
```markdown
# Todo App - Phase I: In-Memory Console

A simple command-line todo list manager built with Python.

## Requirements

- Python 3.11 or higher

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment (see below)
4. No additional dependencies required (uses Python standard library only)

### Activating Virtual Environment

**Windows**: `.venv\Scripts\activate`
**macOS/Linux**: `source .venv/bin/activate`

## Usage

```bash
python src/interface/main.py
```

Follow the on-screen menu to manage your tasks.

## Features

- Add tasks with descriptions
- View all tasks with completion status
- Update task descriptions
- Delete tasks
- Mark tasks as complete or incomplete

## Note

This is an in-memory application. **All tasks are lost when you quit the program.**

## Development

See `specs/001-phase-i-in-memory/quickstart.md` for development setup instructions.

## Testing

```bash
pytest
```

## License

[Your License Here]
```

---

## Development Workflow

### Step 1: Read the Specification

**Before writing any code**, read these documents in order:

1. `specs/001-phase-i-in-memory/spec.md` - **WHAT** to build (user stories, requirements)
2. `specs/001-phase-i-in-memory/plan.md` - **HOW** to build it (architecture, decisions)
3. `specs/001-phase-i-in-memory/data-model.md` - Entity definitions and validation
4. `specs/001-phase-i-in-memory/contracts/cli-menu.md` - CLI behavior specification
5. `specs/001-phase-i-in-memory/research.md` - Technical decisions and rationale

**Time Investment**: 30-45 minutes to read and understand all documents.

**Why**: Constitutional requirement (Spec-Driven Development). Understanding WHAT and WHY before HOW prevents wasted effort.

---

### Step 2: Generate Task List

```bash
# Run the task generation command
/sp.tasks

# This will create specs/001-phase-i-in-memory/tasks.md
# Tasks are organized by user story for independent implementation
```

**Review the task list** before starting implementation. Each task is a discrete unit of work with clear acceptance criteria.

---

### Step 3: Test-First Development

**Constitutional Requirement**: Write tests BEFORE implementation.

**Workflow for Each Task**:

1. **Write Test** (Red phase):
   ```bash
   # Create test file in appropriate directory
   # tests/unit/, tests/integration/, or tests/contract/
   # Write test based on acceptance criteria
   ```

2. **Run Test (should FAIL)**:
   ```bash
   pytest tests/unit/test_task.py -v
   # Verify test fails as expected
   ```

3. **Implement Feature** (Green phase):
   ```bash
   # Write minimal code to make test pass
   # No extra features, just enough to pass the test
   ```

4. **Run Test (should PASS)**:
   ```bash
   pytest tests/unit/test_task.py -v
   # Verify test now passes
   ```

5. **Refactor** (if needed):
   ```bash
   # Clean up code while keeping tests green
   # Run tests after each change
   ```

6. **Commit**:
   ```bash
   git add .
   git commit -m "feat: implement Task entity validation [T001]"
   # Reference task ID in commit message
   ```

---

### Step 4: Run Quality Checks

**Before each commit**, run:

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/

# Run all tests with coverage
pytest
```

**Expected Results**:
- Black: `All done! ✨`
- Ruff: No errors
- Mypy: Success (no type errors)
- Pytest: All tests pass, coverage >= 80%

**Fix any issues** before committing.

---

### Step 5: Manual Testing

**After implementation complete**, test the application manually:

```bash
python src/interface/main.py
```

**Test Scenarios** (from spec User Stories):
1. Add several tasks
2. View task list
3. Mark tasks complete/incomplete
4. Update task descriptions
5. Delete tasks
6. Test error cases (invalid IDs, empty descriptions)

**Time Investment**: 10-15 minutes for complete manual test.

---

## Common Commands Reference

### Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Deactivate
deactivate

# Check Python version
python --version

# Check installed packages
pip list
```

---

### Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_task.py

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run tests matching pattern
pytest -k "test_add"

# Run and stop at first failure
pytest -x
```

---

### Code Quality

```bash
# Format all code
black src/ tests/

# Check formatting without changes
black --check src/ tests/

# Lint code
ruff check src/ tests/

# Lint with auto-fix
ruff check --fix src/ tests/

# Type check
mypy src/

# Type check specific file
mypy src/domain/task.py
```

---

### Git Workflow

```bash
# Check status
git status

# Add changes
git add .

# Commit with message
git commit -m "feat: implement feature [T001]"

# Push to remote
git push origin 001-phase-i-in-memory

# View commit history
git log --oneline

# Create branch for task
git checkout -b feature/task-entity
```

---

## Troubleshooting

### Problem: `python` command not found

**Solution**: Use `python3` instead, or add Python to your PATH.

**Windows**: Reinstall Python and check "Add Python to PATH" during installation.

---

### Problem: Virtual environment activation fails on Windows

**Error**: "Cannot be loaded because running scripts is disabled on this system"

**Solution**:
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activation again
.venv\Scripts\Activate.ps1
```

---

### Problem: `pip install` fails

**Error**: "WARNING: pip is out of date"

**Solution**:
```bash
python -m pip install --upgrade pip
# Then retry package installation
```

---

### Problem: Tests fail with import errors

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
# Ensure you're in project root directory
cd todo-app

# Ensure virtual environment is activated
# Look for (.venv) in prompt

# Install project in editable mode
pip install -e .

# Or add src/ to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"  # Unix/macOS
set PYTHONPATH=%PYTHONPATH%;%CD%\src  # Windows
```

---

### Problem: Mypy shows too many errors

**Issue**: Strict mode is very strict!

**Solution**:
- Fix errors incrementally (start with one module)
- Use `# type: ignore` as last resort (with comment explaining why)
- Ensure all function signatures have type hints
- Import types: `from typing import Optional, Dict, List`

---

### Problem: Black and Ruff disagree on formatting

**Issue**: Conflicting configurations.

**Solution**: Black takes precedence (it's the formatter). Configure Ruff to be compatible:

```toml
[tool.ruff]
line-length = 100  # Match Black's line-length
```

---

## Next Steps

1. ✅ Environment set up → You're ready to implement
2. 📋 Generate tasks → Run `/sp.tasks` to create task list
3. 🧪 Write first test → Start with `tests/unit/test_task.py`
4. ✨ Implement first feature → Task entity in `src/domain/task.py`
5. 🔄 Repeat test-implement cycle → Work through task list
6. 🚀 Manual test → Verify end-to-end user experience
7. 📝 Create PR → Submit for review

---

## Additional Resources

### Documentation
- **Specification**: `specs/001-phase-i-in-memory/spec.md`
- **Architecture**: `specs/001-phase-i-in-memory/plan.md`
- **Data Model**: `specs/001-phase-i-in-memory/data-model.md`
- **CLI Contract**: `specs/001-phase-i-in-memory/contracts/cli-menu.md`

### External Resources
- [Python 3.11 Documentation](https://docs.python.org/3.11/)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://beta.ruff.rs/docs/)

### Constitutional References
- Evolution of Todo Project Constitution v1.0.0
- Spec-Driven Development workflow
- Clean Architecture principles
- Test-First Development requirements

---

## Support

**Questions or Issues?**
- Check troubleshooting section above
- Review specification documents
- Ask team for clarification
- Create issue in project tracker

---

**Status**: ✅ **Quickstart Guide Complete** - Development environment ready!
