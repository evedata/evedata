GIT_ROOT ?= $(shell git rev-parse --show-toplevel)

build:
	uv run build

check: types lint

clean:
	rm -rf dist site .cache .ruff_cache .pytest_cache

docs:
	uv run mkdocs build --strict

fix: fix-markdown fix-python

fix-markdown:
	pnpm run fix:markdown

fix-python:
	uv run ruff check --fix

format: format-python format-turbo

format-python:
	uv run ruff format

format-turbo:
	turbo format

lint: lint-markdown lint-python lint-turbo

lint-markdown:
	pnpm exec markdownlint-cli2 .

lint-python:
	uv run ruff check

lint-turbo:
	turbo lint

pre-commit:
	uv run pre-commit run

pre-commit-all:
	uv run pre-commit run --all-files

publish:
	uv publish

publish-test:
	uv publish --index testpypi

sync:
	uv sync --all-extras --all-groups

test: test-python test-turbo

test-python:
	uv run pytest --cov-branch --cov-report=term-missing --cov-report=lcov tests

test-turbo:
	turbo test

test-benchmark:
	uv run pytest --benchmark-enable tests/benchmarks

test-e2e: test-e2e-python test-e2e-turbo

test-e2e-python:
	uv run pytest tests/e2e

test-e2e-turbo:
	turbo test:e2e

test-integration:
	uv run pytest tests/integration

test-performance:
	uv run pytest tests/performance

test-unit:
	uv run pytest tests/unit

types: types-pyright types-turbo

types-pyright:
	uv run pyright

types-turbo:
	turbo types
