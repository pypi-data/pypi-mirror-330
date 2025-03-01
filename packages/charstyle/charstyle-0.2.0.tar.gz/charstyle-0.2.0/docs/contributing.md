# Contributing to charstyle

Thank you for your interest in contributing to charstyle! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/charstyle.git
   cd charstyle
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## Running Tests

Run the test suite to make sure everything is working correctly:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=charstyle
```

## Code Style

This project follows PEP 8 style guidelines. We use `black` for code formatting and `isort` for import sorting:

```bash
# Format code
black charstyle tests

# Sort imports
isort charstyle tests
```

## Documentation

We use MkDocs for documentation. To build and serve the documentation locally:

```bash
mkdocs serve
```

Then open your browser to http://localhost:8000 to view the documentation.

## Adding New Features

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Implement your feature and add tests.

3. Update the documentation if necessary.

4. Run the tests to make sure everything passes:
   ```bash
   pytest
   ```

5. Submit a pull request.

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

## License

By contributing to charstyle, you agree that your contributions will be licensed under the project's license.
