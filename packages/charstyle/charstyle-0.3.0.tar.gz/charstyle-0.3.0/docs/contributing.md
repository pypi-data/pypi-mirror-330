# Contributing to charstyle

Thank you for your interest in contributing to charstyle! This document provides guidelines and instructions for contributing to the project.

## Development Setup

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
   # Hatch will automatically create the environment when needed
   hatch -e dev run test
   ```

## Running Tests

Run the test suite to make sure everything is working correctly:

```bash
hatch -e dev run test
```

Run tests with coverage:

```bash
hatch -e dev run coverage-report
```

## Code Style

This project follows PEP 8 style guidelines. We use Ruff for code formatting and linting:

```bash
# Format code
hatch -e dev run format

# Lint code
hatch -e dev run lint
```

## Pre-commit Hooks

We use pre-commit hooks to ensure code quality. Install them with:

```bash
hatch -e dev run pre-commit-install
```

## Documentation

We use pdoc for documentation. To build and serve the documentation locally:

```bash
hatch -e dev run docs
```

## Adding New Features

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Implement your feature and add tests.

3. Update the documentation if necessary.

4. Run the tests to make sure everything passes:
   ```bash
   hatch -e dev run test
   ```

5. Run the pre-commit checks:
   ```bash
   hatch -e dev run pre-commit-run
   ```

6. Submit a pull request.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on the GitHub repository. Please include:

- A clear and descriptive title
- A detailed description of the issue or feature request
- Steps to reproduce the issue (if applicable)
- Expected behavior
- Actual behavior
- Environment information (OS, Python version, etc.)

## Style Guidelines

When contributing code, please follow these guidelines:

1. Use descriptive variable and function names.
2. Add docstrings to all functions, classes, and modules.
3. Write clear and concise comments.
4. Follow the existing code style.
5. Include type annotations for all functions and methods.

## License

By contributing to charstyle, you agree that your contributions will be licensed under the project's license.
