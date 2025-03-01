.PHONY: black lint test fmt check

# Set PYTHONPATH to include the project root
export PYTHONPATH := .

# Black configuration
BLACK_ARGS := --line-length 100

# Linting
lint:
	flake8 .

# Formatting
fmt:
	black $(BLACK_ARGS) .

# Testing
test:
	pytest

# Full check (lint + format + test)
check: lint fmt test

# Run tests with coverage report
test-with-coverage:
	pytest --cov=$(PROJECT_NAME) --cov-report=term-missing tests/

# Run Black with verbose output
black-with-output:
	black $(BLACK_ARGS) --verbose
