# charstyle Developer Guide

This guide is intended for developers who want to contribute to or maintain the charstyle library itself. For information on using the library in your applications, see [README.md](README.md).

## Development Environment Setup

### Prerequisites

- Python 3.11 or higher
- [Hatch](https://hatch.pypa.io/) (Python project manager)

### First-time Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/joaompinto/charstyle.git
   cd charstyle
   ```

2. Install Hatch if you don't have it already:
   ```bash
   pip install hatch
   ```

3. Set up the development environment:
   ```bash
   # Hatch will automatically create the development environment when you run commands
   hatch -e dev run test
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
├── LICENSE           # License information
├── README.md         # User documentation
└── CONTRIBUTING.md   # Contribution guidelines
```

## Development Workflow

### Code Style and Quality

This project follows strict code quality guidelines enforced through automated tools:

- **Ruff** for code formatting and linting
- **Mypy** for static type checking

#### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality standards are met before committing changes. This helps catch issues early and maintains consistent code quality.

To set up pre-commit:

```bash
# Install pre-commit hooks
hatch -e dev run pre-commit-install
```

The pre-commit configuration includes:
- Code formatting with Ruff
- Linting with Ruff
- Type checking with MyPy
- Various file checks (YAML, TOML, trailing whitespace, etc.)

You can manually run all pre-commit hooks with:

```bash
# Run pre-commit on all files
hatch -e dev run pre-commit-run
```

#### Formatting and Linting

```bash
# Format code with Ruff
hatch -e dev run format

# Check if code is properly formatted without making changes
hatch -e dev run format-check

# Run linting with auto-fix
hatch -e dev run lint

# Run linting without auto-fix (check only)
hatch -e dev run lint-check

# Run linting with unsafe auto-fixes
hatch -e dev run lint-all

# Run type checking
hatch -e dev run typecheck
```

### Testing

All new features and bug fixes should include tests. We use Python's built-in unittest framework.

```bash
# Run all tests
hatch -e dev run test

# Run tests with coverage report
hatch -e dev run coverage-report

# Generate HTML coverage report
hatch -e dev run coverage-html
```

### Running Examples

Examples demonstrate the library's features and serve as usage documentation.

```bash
# Run all examples
hatch -e dev run examples

# Run a specific example
hatch -e dev run example basic_usage.py
```

### Documentation

Code should be well-documented with docstrings. The project uses pdoc for generating API documentation from docstrings.

```bash
# Generate HTML documentation
hatch -e dev run docs
```

### Combined Workflow Tasks

For convenience, several combined tasks are available:

```bash
# Run pre-commit checks (format, lint, test)
hatch -e dev run pre-commit

# Run all checks without modifying files
hatch -e dev run check-all
```

### Cleanup

```bash
# Clean up build artifacts and cache files
hatch -e dev run clean
```

## Building and Publishing

### Building the Package

```bash
# Build source distribution and wheel
hatch -e dev run build
```

The built packages will be available in the `dist/` directory.

### Publishing

```bash
# Publish to PyPI
hatch -e dev run publish

# Publish to Test PyPI for testing
hatch -e dev run publish-test
```

## Development Guidelines

### Adding Dependencies

Hatch manages dependencies through the `pyproject.toml` file. The project is configured with separate environments:

- `default`: Minimal dependencies needed for users
- `dev`: All development tools and dependencies

To add a dependency, edit the appropriate section in `pyproject.toml`:

```toml
# For runtime dependencies (used by library users)
[project]
dependencies = [
    # Add dependencies here
]

# For development dependencies
[tool.hatch.envs.dev]
dependencies = [
    # Add dev dependencies here
]
```

### Using uv for Faster Dependency Management

The project is configured to use [uv](https://github.com/astral-sh/uv) for faster dependency resolution and installation. You can use the following commands:

```bash
# Install a package with uv
hatch -e dev run uv-install package_name

# Export dependencies to requirements.txt
hatch -e dev run uv-export

# Sync dependencies from requirements.txt
hatch -e dev run uv-sync
```

### Type Annotations

All new code should include proper type annotations. The project uses mypy with strict settings to enforce type correctness.

### Pull Request Process

1. Create a new branch for your feature or bugfix
2. Make your changes, including tests and documentation
3. Ensure all tests pass and code quality checks succeed
4. Submit a pull request to the main repository

### Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md with the changes
3. Build the package: `hatch -e dev run build`
4. Test the package installation from the built wheel
5. Publish to PyPI: `hatch -e dev run publish`
6. Create a git tag for the version
7. Update the release notes on GitHub

## Troubleshooting

### Common Issues

- **Hatch environment issues**: Try removing `.venv` and running `hatch -e dev run test` again
- **Import errors in tests**: Ensure you're running tests via `hatch -e dev run test` rather than directly

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [Hatch Documentation](https://hatch.pypa.io/)
- [Ruff Documentation](https://github.com/astral-sh/ruff)
- [Mypy Documentation](https://mypy.readthedocs.io/)
