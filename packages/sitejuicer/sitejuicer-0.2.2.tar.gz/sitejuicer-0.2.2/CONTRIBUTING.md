# Contributing to SiteJuicer

Thank you for your interest in contributing to SiteJuicer! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

There are many ways to contribute to SiteJuicer:

1. **Reporting Bugs**: If you find a bug, please create an issue with a detailed description of the problem, steps to reproduce, and your environment.

2. **Suggesting Enhancements**: Have an idea for a new feature? Create an issue with the tag "enhancement" and describe your proposal.

3. **Code Contributions**: Want to fix a bug or implement a feature? Follow the steps below.

## Development Workflow

1. **Fork the Repository**: Create your own fork of the repository.

2. **Clone Your Fork**: 
   ```bash
   git clone https://github.com/your-username/SiteJuicer.git
   cd SiteJuicer
   ```

3. **Set Up Development Environment**:
   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -e ".[all,dev]"
   ```

4. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make Your Changes**: Implement your changes, following the code style guidelines.

6. **Run Tests**:
   ```bash
   # Run tests
   pytest
   
   # Check code style
   flake8
   black --check .
   isort --check .
   ```

7. **Commit Your Changes**:
   ```bash
   git commit -m "Add a descriptive commit message"
   ```

8. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

9. **Create a Pull Request**: Go to the original repository and create a pull request from your branch.

## Code Style Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
- Use [Black](https://black.readthedocs.io/) for code formatting.
- Use [isort](https://pycqa.github.io/isort/) for import sorting.
- Write docstrings for all functions, classes, and modules.
- Include type hints where appropriate.
- Write unit tests for new functionality.

## Pull Request Process

1. Ensure your code passes all tests and style checks.
2. Update documentation if necessary.
3. The PR should work for Python 3.7 and above.
4. Your PR will be reviewed by maintainers, who may request changes.
5. Once approved, your PR will be merged.

## Release Process

Releases are managed by the project maintainers. The process typically involves:

1. Updating the version number in `__init__.py`.
2. Updating the CHANGELOG.md file.
3. Creating a new release on GitHub.
4. Publishing to PyPI.

## Questions?

If you have any questions about contributing, feel free to open an issue for clarification.

Thank you for contributing to SiteJuicer! 