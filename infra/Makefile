check: types lint

clean:
	rm -rf .ruff_cache .pytest_cache

fix: fix-markdown fix-python

fix-markdown:
	pnpm run fix:markdown

fix-python:
	uv run ruff check --fix

format: format-markdown format-python format-toml

format-markdown:
	pnpm run format:markdown

format-python:
	uv run ruff format

format-toml:
	pnpm run format:toml

lint: lint-markdown lint-python lint-terraform lint-yaml

lint-markdown:
	pnpm run lint:markdown

lint-python:
	uv run ruff check

lint-terraform:
	tflint --chdir terraform --recursive -f compact

lint-yaml:
	uv run yamllint --strict .

types:
	uv run pyright
