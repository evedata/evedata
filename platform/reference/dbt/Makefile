.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: dbt-debug
dbt-debug: ## Run dbt debug to test connection and configuration
	uv run dbt debug

.PHONY: dbt-deps
dbt-deps: ## Install dbt dependencies
	uv run dbt deps

.PHONY: dbt-seed
dbt-seed: ## Load seed data into the warehouse
	uv run dbt seed

.PHONY: dbt-run
dbt-run: ## Run all dbt models
	uv run dbt run

.PHONY: dbt-run-models
dbt-run-models: ## Run specific models (use MODELS=model_name)
	uv run dbt run --models $(MODELS)

.PHONY: dbt-run-full
dbt-run-full: ## Run full refresh of all models
	uv run dbt run --full-refresh

.PHONY: dbt-test
dbt-test: ## Run all dbt tests
	uv run dbt test

.PHONY: dbt-test-models
dbt-test-models: ## Test specific models (use MODELS=model_name)
	uv run dbt test --models $(MODELS)

.PHONY: dbt-snapshot
dbt-snapshot: ## Run dbt snapshots
	uv run dbt snapshot

.PHONY: dbt-compile
dbt-compile: ## Compile dbt models without running
	uv run dbt compile

.PHONY: dbt-clean
dbt-clean: ## Clean dbt artifacts
	uv run dbt clean

.PHONY: dbt-docs-generate
dbt-docs: ## Generate dbt documentation
	uv run dbt docs generate

.PHONY: dbt-docs-serve
dbt-docs-serve: ## Serve dbt documentation locally
	uv run dbt docs serve

.PHONY: dbt-evaluate
dbt-evaluate: ## Evaluate dbt project for best practices
	uv run dbt build --select package:dbt_project_evaluator

.PHONY: dbt-list
dbt-list: ## List all resources in the dbt project
	uv run dbt list

.PHONY: dbt-list-models
dbt-list-models: ## List all models in the dbt project
	uv run dbt list --resource-type model

.PHONY: dbt-list-tests
dbt-list-tests: ## List all tests in the dbt project
	uv run dbt list --resource-type test

.PHONY: dbt-build
dbt-build: ## Run seeds, models, snapshots, and tests
	uv run dbt build

.PHONY: dbt-build-models
dbt-build-models: ## Build specific models with tests (use MODELS=model_name)
	uv run dbt build --models $(MODELS)

.PHONY: dbt-source-freshness
dbt-source-freshness: ## Check source data freshness
	uv run dbt source freshness

.PHONY: dbt-parse
dbt-parse: ## Parse the dbt project and generate manifest
	uv run dbt parse

# Composite DBT Tasks
.PHONY: dbt-init
dbt-init: dbt-deps dbt-seed ## Initialize dbt project (install deps and load seeds)

.PHONY: dbt-refresh
dbt-refresh: dbt-clean dbt-deps dbt-run-full dbt-test ## Full refresh: clean, deps, run, test

.PHONY: dbt-ci
dbt-ci: dbt-deps dbt-compile dbt-test ## CI pipeline: deps, compile, test
