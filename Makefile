.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: fix
fix: fix-python ## Fix all files

.PHONY: fix-markdown
fix-markdown: ## Fix Markdown files
	pnpm run fix:markdown

.PHONY: fix-python
fix-python: ## Fix Python files
	uv run ruff check --fix .

.PHONY: format
format: format-python ## Format all files

.PHONY: format-prettier
format-prettier: ## Format all files with Prettier
	pnpm run format:prettier

.PHONY: format-python
format-python: ## Format Python files
	uv run ruff format .

.PHONY: lint
lint: lint-python  ## Lint all files

.PHONY: lint-markdown
lint-markdown: ## Lint Markdown files
	pnpm run lint:markdown

.PHONY: lint-python
lint-python: ## Lint Python files
	uv run ruff check .

.PHONY: types
types: types-python ## Check types for all files

.PHONY: types-python
types-python: ## Check types for Python files
	uv run pyright
