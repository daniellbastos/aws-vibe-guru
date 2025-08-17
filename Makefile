# Development commands
lint:
	uv run ruff check src/

lint-fix:
	uv run ruff check src/ --fix

format:
	uv run ruff format src/

format-check:
	uv run ruff format src/ --check

quality: lint format
	@echo "✅ Code quality checks completed"

install-dev:
	uv sync --extra dev

pre-commit-install:
	uv run pre-commit install

pre-commit-update:
	uv run pre-commit autoupdate

pre-commit-run:
	uv run pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf dist/ build/ *.egg-info/ 2>/dev/null || true

# PyPI publishing commands
build:
	uv run python -m build

check-dist:
	uv run twine check dist/*

upload-test:
	uv run twine upload --repository testpypi dist/*

upload-pypi:
	uv run twine upload dist/*

publish-test: build check-dist upload-test
	@echo "✅ Package published to TestPyPI"

publish: build check-dist upload-pypi
	@echo "✅ Package published to PyPI"
