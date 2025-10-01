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

publish-test: clean build check-dist upload-test
	@echo "✅ Package published to TestPyPI"

publish: clean build check-dist upload-pypi
	@echo "✅ Package published to PyPI"

release-check:
	@echo "🔍 Checking release requirements..."
	@if [ -z "$$(git status --porcelain)" ]; then \
		echo "✅ Working directory is clean"; \
	else \
		echo "❌ Working directory has uncommitted changes"; \
		exit 1; \
	fi
	@echo "✅ Git status OK"
	@VERSION=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2); \
	if git tag | grep -q "v$$VERSION"; then \
		echo "✅ Git tag exists for current version (v$$VERSION)"; \
	else \
		echo "❌ Git tag missing for current version (v$$VERSION)"; \
		exit 1; \
	fi
	@echo "✅ All checks passed"

release-test: release-check publish-test
	@echo ""
	@echo "🎉 Test release completed successfully!"
	@echo ""
	@echo "📦 Test installation:"
	@echo "   pip install -i https://test.pypi.org/simple/ aws-vibe-guru"
	@echo ""

release: release-check publish
	@echo ""
	@echo "🎉 Release completed successfully!"
	@echo ""
	@echo "📦 Installation:"
	@echo "   pip install aws-vibe-guru"
	@echo ""
	@echo "🔗 PyPI: https://pypi.org/project/aws-vibe-guru/"
	@echo ""
