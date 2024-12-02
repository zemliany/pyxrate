# Makefile for managing the project

.PHONY: help check-poetry check-token check-python check-token lock dependencies env test format lint

help: # Show available commands and descriptions
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*#"} /^[a-zA-Z\-_]+:.*#/ { \
		printf "  %-15s %s\n", $$1, $$2 \
	}' $(MAKEFILE_LIST)

# Check if poetry is installed
check-poetry:
	@if ! command -v poetry >/dev/null 2>&1; then \
		echo "Error: Poetry is not installed. Please install it from https://python-poetry.org/"; \
		exit 1; \
	fi

# Check if Python is installed
check-python:
	@if ! command -v python >/dev/null 2>&1; then \
		echo "Error: Python is not installed. Please install Python."; \
		exit 1; \
	fi

# Check if the TEST_PYPI_TOKEN environment variable is set
check-test-token:
	@if [ -z "$$TEST_PYPI_TOKEN" ]; then \
		echo "Error: TEST_PYPI_TOKEN environment variable is not set. Please export your Test PyPI token."; \
		exit 1; \
	fi

# Check if the PROD_PYPI_TOKEN environment variable is set
check-prod-token:
	@if [ -z "$$PROD_PYPI_TOKEN" ]; then \
		echo "Error: PROD_PYPI_TOKEN environment variable is not set. Please export your Production PyPI token."; \
		exit 1; \
	fi

# Set up Test PyPI repository
setup-test-pypi: check-test-token
	@if ! poetry config --list | grep -q "repositories.testpypi"; then \
		echo "======= Configuring Test PyPI repository in Poetry... ======="; \
		poetry config repositories.testpypi https://test.pypi.org/legacy/; \
		echo "Configuring Test PyPI credentials..."; \
		poetry config pypi-token.testpypi $$TEST_PYPI_TOKEN; \
		echo "======= Test PyPI repository configured successfully! =======\n"; \
	else \
		echo "======= Test PyPI repository is already configured. =======\n"; \
	fi

# Set up Production PyPI repository
setup-prod-pypi: check-prod-token
	@if ! poetry config --list | grep -q "repositories.pypi"; then \
		echo "======= Configuring Production PyPI repository in Poetry... ======="; \
		poetry config repositories.pypi https://upload.pypi.org/legacy/; \
		echo "Configuring Production PyPI credentials..."; \
		poetry config pypi-token.pypi $$PROD_PYPI_TOKEN; \
		echo "======= Production PyPI repository configured successfully! =======\n"; \
	else \
		echo "======= Production PyPI repository is already configured. =======\n"; \
	fi

# Command to generate a poetry lock file
lock: check-poetry # Generate a new Poetry lock file
	poetry lock

# Command to update dependencies
dependencies: check-poetry # Update project dependencies
	poetry update --no-cache

# Command to set up the local environment
env: check-poetry # Set up the development environment
	poetry install
	poetry shell

# Run tests
test: check-python # Run unit tests
	@echo "======= Running tests with unittest... ======="
	python -m unittest tests/test_currency_converter.py
	@echo "======= Tests completed =======\n"

# Command to run black for formatting
format: # Format code with Black
	@echo "======= Running black for code formatting... ======= "
	black . --skip-string-normalization --line-length 120
	@echo "======= Code formatting completed successfully.=======\n"

lint: # Lint the codebase
	@echo "======= Running lint for code... ======="
	poetry run flake8 --max-line-length=120 --ignore=E731
	@echo "======= Code linting completed successfully. =======\n"

coverage: # Check coverage the codebase
	@echo "======= Running coverage for code... ======="
	coverage run --omit="*/__init__.py,*/tests/*" -m unittest discover -s tests
	coverage report --fail-under=75
	@echo "======= Code coverage completed successfully. =======\n"

patch: # Increment package version
	@echo "Patching package version..."
	poetry version patch

# Publish the package to Test PyPI
publish-test: setup-test-pypi test lint format # Publish package to Test PyPI (test.pypi.org)
	@echo "+++++++ Publishing the package to Test PyPI... +++++++"
	poetry publish --build --repository testpypi
	@echo "+++++++ Package published to Test PyPI successfully! +++++++"

# Publish the package to PyPI
publish-prod: setup-prod-pypi test lint format # Publish package to PyPI (pypi.org)
	@echo "+++++++ Publishing the package to PyPI... +++++++"
	poetry publish --build --repository pypi
	@echo "+++++++ Package published to PyPI successfully! +++++++"
