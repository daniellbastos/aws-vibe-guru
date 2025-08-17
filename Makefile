run:
	uv run python -m aws_toolbelt.cli $(CMD) $(ARGS)

hello:
	uv run python -m aws_toolbelt.cli hello

hello-name:
	uv run python -m aws_toolbelt.cli --name "Developer"

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

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
