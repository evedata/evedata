# EVEData Development Standards

## Repository structure

- @docs/: EVEData documentation site
  - @docs/content: Markdown source files for documentation
- @infra/: Infrastructure-as-code configuration and automation
  - @infra/ansible: Ansible inventory, playbooks, roles, and plugins for bare metal provisioning
  - @infra/tofu: OpenTofu modules for cloud provisioning
- @platform/: Main platform packages
  - @platform/admin/ (evedata-platform-admin): Administration CLI, REST API, and maintenance tasks
  - @platform/admin-core/ (evedata-platform-admin-core): Shared library for platform components that implement administration CLI commands, REST API endpoints, and maintenance tasks
  - @platform/core/ (evedata-platform-core): Shared library for all platform components with configuration, logging, metrics, and other utilities
  - @platform/datasets (evedata-platform-datasets): User-facing REST API for serving EVEData datasets
  - @platform/extract (evedata-platform-extract): DLT pipelines for raw data extraction (e.g. market orders, static data)
  - @platform/rest (evedata-platform-rest): User-facing REST API
  - @platform/rest-core (evedata-platform-rest-core): Shared library for platform components that implement user-facing REST API endpoints
  - @platform/transform (evedata-platform-transform): DBT project for data transform
  - @platform/utils (evedata-platform-utils): Shared library with utilities
  - @platform/web: User-facing web application (Ruby on Rails)

## Common commands

### Python package-specific commands

- MANDATORY: ALWAYS run `cd $EVEDATA_HOME` before running Python-related commands for a specific package
- ALWAYS include `--directory` and `--package` when running `uv` commands
  - BAD example: `cd platform/utils && uv run pytest`
  - GOOD example: `uv run --directory platform/utils --package evedata-platform-utils pytest
- Check types for all Python files in a package: `uv run --directory platform/utils --package evedata-platform-utils pyright`
- Check types for specific Python files in a package: `uv run --directory platform/utils --package evedata-platform-utils pyright <filename ...>`
- Lint, fix, and format all Python files in a package: `uv run --directory platform/utils --package evedata-platform-utils ruff check --fix && uv run --directory platform/utils --package evedata-platform-utils ruff format`
- Lint, fix, and format specific Python files in a package: `uv run --directory platform/utils --package evedata-platform-utils ruff check --fix <filename ...> && uv run --directory platform/utils --package evedata-platform-utils ruff format <filename ...>`
- Run all tests in a package: `uv run --directory platform/utils --package evedata-platform-utils pytest`
- Run specific test files in a package: `uv run --directory platform/utils --package evedata-platform utils pytest <filename ...>`
- Run specific test function in a package: `uv run --directory platform/utils --package evedata-platform-utils pytest tests/test_mod.py::test_func`
- Run specific test function with parameterization in a package: `uv run --directory platform/utils --package evedata-platform-utils pytest tests/test_mod.py::test_func[x1,y2]`
- Run all tests in a class in a package: `uv run --directory platform/utils --package evedata-platform-utils pytest tests/test_mod.py::TestClass`
- Run specific test method in a package: `uv run --directory platform/utils --package evedata-platform-utils pytest tests/test_mod.py::TestClass::test_method`
- Run specific test method with parameterization in a package: `uv run --directory platform/utils --package evedata-platform-utils pytest tests/test_mod.py::TestClass::test_method[x1,y2]`
- Run tests by marker expressions in a package: `uv run --directory platform/utils --package evedata-platform-utils pytest -m slow`

### Project-wide commands

- MANDATORY: ALWAYS run `cd $EVEDATA_HOME` before running project-wide commands
- Sync Python dependencies: `make sync-python`
- Lint, fix, and format all Python files: `make fix-python format-python`
- Lint, fix, and format Python files: `uv run ruff check --fix <filename ...> && uv run ruff format <filename ...>`
- Run Python scripts: `uv run python <script>`
- Run `evedatactl` Administration CLI: `uv run evedatactl`
