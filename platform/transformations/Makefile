.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: build
dbt-build: ## Build all transformations
	uv run dbt build

.PHONY: compile
dbt-compile: ## Compile all transformations
	uv run dbt compile

.PHONY: dbt-deps
dbt-deps: ## Install dbt dependencies
	uv run dbt deps

.PHONY: dbt-run
dbt-run: ## Run all transformations
	uv run dbt run

.PHONY: dbt-snapshot
dbt-snapshot: ## Snapshot all transformations
	uv run dbt snapshot

.PHONY: fix
fix: fix-python fix-sql ## Fix all files

.PHONY: fix-python
fix-python: ## Fix Python files
	uv run ruff check --fix .

.PHONY: fix-sql
fix-sql: ## Fix SQL files
	uv run sqlfluff fix .

.PHONY: format
format: format-python format-sql ## Format all files

.PHONY: format-python
format-python: ## Format Python files
	uv run ruff format .

.PHONY: format-sql
format-sql: ## Format SQL files
	uv run sqlfmt .

.PHONY: lint
lint: lint-python lint-sql ## Lint all files

.PHONY: lint-dbt
lint-dbt: ## Lint dbt project files
	uv run dbt parse

.PHONY: lint-python
lint-python: ## Lint Python files
	uv run ruff check .

.PHONY: lint-sql
lint-sql: ## Lint SQL files
	uv run sqlfluff lint

.PHONY: test
test: test-dbt ## Run all tests

.PHONY: test-dbt
test-dbt: ## Test all transformations
	uv run dbt test --exclude package:dbt_project_evaluator

.PHONY: test-data
test-data: ## Run data tests for all transformations
	uv run dbt test --select test_type:data --exclude package:dbt_project_evaluator

.PHONY: test-unit-dbt
test-unit-dbt: ## Run unit tests for all transformations
	uv run dbt test --select test_type:unit --exclude package:dbt_project_evaluator

.PHONY: types
types: types-python ## Check types for all files

.PHONY: types-python
types-python: ## Check types for Python files
	uv run pyright
