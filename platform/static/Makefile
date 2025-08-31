.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: extract-esi
extract-esi: ## Load ESI raw data into the warehouse
	uv run evedatactl static extract esi

.PHONY: extract-hde
extract-hde: ## Load HDE raw data into the warehouse
	uv run evedatactl static extract hde

.PHONY: extract-sde
extract-sde: ## Load SDE raw data into the warehouse
	uv run evedatactl static extract sde

.PHONY: fix
fix: fix-python ## Fix all files

.PHONY: fix-python
fix-python: ## Fix Python files
	uv run ruff check --fix .

.PHONY: format
format: format-python ## Format all files

.PHONY: format-python
format-python: ## Format Python files
	uv run ruff format .

.PHONY: lint
lint: lint-python  ## Lint all files

.PHONY: lint-python
lint-python: ## Lint Python files
	uv run ruff check .

.PHONY: test
test: ## Run all tests
	uv run pytest

.PHONY: types
types: types-python ## Check types for all files

.PHONY: types-python
types-python: ## Check types for Python files
	uv run pyright
