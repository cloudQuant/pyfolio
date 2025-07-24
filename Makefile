.PHONY: help install install-dev test test-all lint format clean build docs

help:
	@echo "Available commands:"
	@echo "  install       Install pyfolio in production mode"
	@echo "  install-dev   Install pyfolio in development mode with all dependencies"
	@echo "  test          Run tests with pytest"
	@echo "  test-all      Run tests on all Python versions with tox"
	@echo "  lint          Check code style and quality"
	@echo "  format        Auto-format code with black and isort"
	@echo "  clean         Remove build artifacts"
	@echo "  build         Build distribution packages"
	@echo "  docs          Build documentation"

install:
	pip install -r requirements-empyrical.txt
	pip install -e .

install-dev:
	pip install -r requirements-empyrical.txt
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest tests/ -v --cov=pyfolio --cov-report=term

test-all:
	tox

lint:
	flake8 pyfolio
	black --check pyfolio
	isort --check-only pyfolio
	mypy pyfolio

format:
	black pyfolio
	isort pyfolio

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .tox/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

docs:
	cd docs && make html