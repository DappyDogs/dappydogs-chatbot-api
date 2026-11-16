ifeq ($(OS),Windows_NT)
PYTHON ?= .venv/Scripts/python.exe
else
PYTHON ?= .venv/bin/python
endif

PYTHON_PATHS ?= src tests

.PHONY: help install-dev format format-check lint test check

help:
	@echo "Available targets:"
	@echo "  install-dev   Install the project with development dependencies"
	@echo "  format        Format Python sources with Ruff"
	@echo "  format-check  Check Python formatting with Ruff"
	@echo "  lint          Run Ruff lint checks"
	@echo "  test          Run the pytest suite"
	@echo "  check         Run formatting, lint, and tests"

install-dev:
	$(PYTHON) -m pip install --editable ".[dev]"

format:
	$(PYTHON) -m ruff format $(PYTHON_PATHS)
	$(PYTHON) -m ruff check --fix $(PYTHON_PATHS)

format-check:
	$(PYTHON) -m ruff format --check $(PYTHON_PATHS)

lint:
	$(PYTHON) -m ruff check $(PYTHON_PATHS)

test:
	$(PYTHON) -m pytest

check: format-check lint test
