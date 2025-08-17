run:
	uv run python -m aws_toolbelt.cli $(CMD) $(ARGS)

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

test:
	uv run pytest

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
