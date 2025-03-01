# Contributing to charstyle

Thank you for your interest in contributing to charstyle!

## Development Setup

### Prerequisites

- Python 3.11 or higher
- [PDM](https://pdm.fming.dev/) (Python Dependency Manager)

### First-time Setup

1. Install PDM if you don't have it already:
   ```bash
   pip install pdm
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/joaompinto/charstyle.git
   cd charstyle
   ```

3. Install dependencies:
   ```bash
   pdm install
   ```

## Development Workflow

### Running Tests

```bash
pdm run test
```

### Linting

Check code with Ruff:
```bash
pdm run lint
```

Automatically fix linting issues:
```bash
pdm run lint-fix
```

### Running Examples

```bash
pdm run python examples/basic_usage.py
```

## Code Style

This project uses:

- [Ruff](https://github.com/astral-sh/ruff) for linting and fixing code style issues
- [Black](https://github.com/psf/black) for code formatting

To ensure your code matches the project style, run the following commands before submitting a PR:

```bash
# Format code
pdm run format

# Run linting (with auto-fix)
pdm run lint
```

You can also check if your code would pass CI checks without modifying files:

```bash
# Check formatting
pdm run format-check

# Check linting
pdm run lint-check
```

- Use enum-based styling for all new code.
- Follow PEP 8 guidelines for code style.
- Add docstrings for all public functions, classes, and methods.
- Make sure all tests pass before submitting a pull request.

## Pull Request Process

1. Ensure all tests pass and code is linted.
2. Update documentation if needed.
3. Create a pull request with a clear description of the changes.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).
