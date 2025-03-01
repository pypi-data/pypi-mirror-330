# charstyle Developer Guide

This guide is intended for developers who want to contribute to or maintain the charstyle library itself. For information on using the library in your applications, see [README.md](README.md).

## Development Environment Setup

### Prerequisites

- Python 3.11 or higher
- [PDM](https://pdm.fming.dev/) (Python Dependency Manager)

### First-time Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/joaompinto/charstyle.git
   cd charstyle
   ```

2. Install PDM if you don't have it already:
   ```bash
   pip install pdm
   ```

3. Set up the development environment:
   ```bash
   pdm install
   ```

## Project Structure

```
charstyle/
├── examples/         # Example scripts demonstrating library features
├── charstyle/        # Core package
│   ├── __init__.py   # Package initialization and exports
│   ├── charstyle.py  # Core styling functionality
│   ├── styles.py     # Style enums and constants
│   ├── icons.py      # Terminal icons
│   └── complex_style.py # Advanced styling functionality
├── tests/            # Unit tests
├── pyproject.toml    # Project configuration and dependencies
├── pdm.toml          # PDM-specific configuration
├── LICENSE           # License information
├── README.md         # User documentation
└── CONTRIBUTING.md   # Contribution guidelines
```

## Development Workflow

### Code Style and Quality

This project follows strict code quality guidelines enforced through automated tools:

- **Black** for code formatting
- **Ruff** for linting and code quality checks
- **Mypy** for static type checking

#### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality standards are met before committing changes. This helps catch issues early and maintains consistent code quality.

To set up pre-commit:

```bash
# Option 1: Using the setup script (recommended)
python scripts/setup_pre_commit.py

# Option 2: Manual installation
pdm run pre-commit-install
```

The pre-commit configuration includes:
- Code formatting with Black
- Linting with Ruff
- Type checking with MyPy
- Various file checks (YAML, TOML, trailing whitespace, etc.)

You can manually run all pre-commit hooks with:

```bash
pdm run pre-commit-run
# or directly
pre-commit run --all-files
```

#### Formatting and Linting

```bash
# Format code with Black
pdm run format

# Check if code is properly formatted without making changes
pdm run format-check

# Run linting with auto-fix
pdm run lint

# Run linting without auto-fix (check only)
pdm run lint-check

# Run linting with unsafe auto-fixes
pdm run lint-all

# Run type checking
pdm run typecheck
```

### Testing

All new features and bug fixes should include tests. We use Python's built-in unittest framework.

```bash
# Run all tests
pdm run test

# Run tests with coverage report
pdm run coverage

# Generate HTML coverage report
pdm run coverage-html
```

### Running Examples

Examples demonstrate the library's features and serve as usage documentation.

```bash
# Run all examples
pdm run examples

# Run a specific example
pdm run example basic_usage.py
```

### Documentation

Code should be well-documented with docstrings. The project uses pdoc for generating API documentation from docstrings.

```bash
# Generate HTML documentation
pdm run docs
```

### Combined Workflow Tasks

For convenience, several combined tasks are available:

```bash
# Run pre-commit checks (format, lint, test)
pdm run pre-commit

# Run all checks without modifying files
pdm run check-all
```

### Cleanup

```bash
# Clean up build artifacts and cache files
pdm run clean
```

## Building and Publishing

### Building the Package

```bash
# Build source distribution and wheel
pdm run build
```

The built packages will be available in the `dist/` directory.

### Publishing

```bash
# Publish to PyPI
pdm run publish

# Publish to Test PyPI for testing
pdm run publish-test
```

## Development Guidelines

### Adding Dependencies

PDM manages dependencies through the `pyproject.toml` file:

```bash
# Add a runtime dependency
pdm add package_name

# Add a development dependency
pdm add -d package_name
```

### Type Annotations

All new code should include proper type annotations. The project uses mypy with strict settings to enforce type correctness.

### Git Workflow

1. Create a feature branch from `main`
2. Implement your changes with appropriate tests
3. Run pre-commit checks: `pdm run pre-commit`
4. Submit a pull request

### Version Control Practices

- Use clear, descriptive commit messages
- Keep pull requests focused on a single feature or bug fix
- Reference issue numbers in commit messages and pull requests

## Release Process

1. Update the version in `pyproject.toml`
2. Run all checks: `pdm run check-all`
3. Build the package: `pdm run build`
4. Test the package installation from the built wheel
5. Publish to PyPI: `pdm run publish`
6. Create a git tag for the version
7. Update the release notes on GitHub

## Troubleshooting

### Common Issues

- **PDM environment issues**: Try removing `.venv` and running `pdm install` again
- **Import errors in tests**: Ensure you're running tests via `pdm run test` rather than directly

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PDM Documentation](https://pdm.fming.dev/)
- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://github.com/astral-sh/ruff)
- [Mypy Documentation](https://mypy.readthedocs.io/)
