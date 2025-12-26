.PHONY: help install install-dev lint format test test-all coverage docs docs-serve build clean pre-commit

# Default target
help:
	@echo "Wabi Sphinx Theme - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install       Install package in development mode"
	@echo "  install-dev   Install with all dev dependencies"
	@echo ""
	@echo "Quality:"
	@echo "  lint          Run ruff linter"
	@echo "  format        Format code with ruff"
	@echo "  typecheck     Run mypy type checking"
	@echo "  pre-commit    Run all pre-commit hooks"
	@echo ""
	@echo "Testing:"
	@echo "  test          Run tests (excluding slow/integration)"
	@echo "  test-all      Run all tests including integration"
	@echo "  coverage      Run tests with coverage report"
	@echo ""
	@echo "Documentation:"
	@echo "  docs          Build documentation"
	@echo "  docs-serve    Serve documentation with auto-reload"
	@echo ""
	@echo "Build:"
	@echo "  build         Build package"
	@echo "  clean         Clean build artifacts"

# Setup
install:
	uv sync

install-dev:
	uv sync --all-extras

# Quality
lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

format:
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/

typecheck:
	uv run mypy src/

pre-commit:
	uv run pre-commit run --all-files

# Testing
test:
	uv run pytest -m "not slow and not integration" --cov-fail-under=0

test-all:
	uv run pytest --cov-fail-under=0

coverage:
	uv run pytest --cov-report=html --cov-fail-under=0
	@echo "Coverage report: coverage_html/index.html"

# Documentation
docs:
	uv run sphinx-build -b html docs docs/_build/html

docs-serve:
	uv run sphinx-autobuild docs docs/_build/html --open-browser

# Build
build:
	uv build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/*.egg-info/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf coverage_html/
	rm -rf docs/_build/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
