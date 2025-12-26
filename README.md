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
python -m src.interface.main
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

MIT License
# Todo-app CLI
