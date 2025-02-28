# Contributing to Manticore CockroachDB

Thank you for your interest in contributing to the Manticore CockroachDB client! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/manticoretechnology/manticore-cockroachdb.git
   cd manticore-cockroachdb
   ```

2. Create a virtual environment and install development dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev,docs]"
   ```

3. Install pre-commit hooks (recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

2. Make your changes, ensuring you follow the code style guidelines

3. Add tests for your changes

4. Run the tests to make sure everything works:
   ```bash
   pytest
   ```

5. Run type checking:
   ```bash
   mypy manticore_cockroachdb
   ```

6. Format your code:
   ```bash
   black manticore_cockroachdb tests
   isort manticore_cockroachdb tests
   ```

7. Commit your changes with a descriptive message:
   ```bash
   git commit -am "Add new feature: your feature description"
   ```

8. Push your branch and create a pull request

## Code Style Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Sort imports with [isort](https://pycqa.github.io/isort/)
- Include type annotations for all function parameters and return values
- Write docstrings in the Google style format

## Testing

- Write tests for all new features and bug fixes
- Ensure all tests pass before submitting a pull request
- Aim for high test coverage (>90%)
- Include both synchronous and asynchronous tests where applicable

## Documentation

- Update documentation for any new features or changes to existing functionality
- Documentation is built with MkDocs and the Material theme
- To preview documentation locally:
  ```bash
  mkdocs serve
  ```
- Document all public API methods with clear examples

## Submitting a Pull Request

1. Ensure your code passes all tests and quality checks
2. Update documentation as needed
3. Include a clear description of the changes in your pull request
4. Link any related issues in the pull request description
5. Wait for code review and address any feedback

## Building and releasing

1. Ensure all tests pass
2. Update version number in:
   - `manticore_cockroachdb/__init__.py`
   - `setup.py`
   - `pyproject.toml`
3. Update `CHANGELOG.md` with the new version and changes
4. Build the package:
   ```bash
   python -m build
   ```
5. Test the built package:
   ```bash
   pip install dist/*.whl
   ```
6. Upload to PyPI (maintainers only):
   ```bash
   twine upload dist/*
   ```

## Code of Conduct

Please be respectful and considerate of others when contributing to the project. We aim to create a welcoming and inclusive environment for all contributors. 