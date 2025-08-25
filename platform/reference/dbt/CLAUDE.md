# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# EVE Static - dbt Project

This is the dbt project for EVE Static, which transforms EVE Online's Static Data Export (SDE) into analytical models using DuckDB.

## Essential Commands

Working from the `/dbt` directory:

### Common dbt Commands
- `uv run dbt debug`: Test connection and configuration
- `uv run dbt deps`: Install dbt dependencies
- `uv run dbt run`: Run all models
- `uv run dbt test`: Run all tests
- `uv run dbt build`: Run seeds, models, snapshots, and tests
- `uv run dbt docs generate`: Generate documentation
- `uv run dbt docs serve`: Serve documentation locally

### Model Development
- `uv run dbt run --models model_name`: Run specific model
- `uv run dbt run --models +model_name`: Run model and its dependencies
- `uv run dbt run --models model_name+`: Run model and its downstream models
- `uv run dbt test --models model_name`: Test specific model
- `uv run dbt compile`: Compile models without running

### Makefile Shortcuts (if available locally)
- `make dbt-init`: Initialize project (deps + seeds)
- `make dbt-refresh`: Full refresh (clean + deps + run + test)
- `make dbt-run-models MODELS=model_name`: Run specific models
- `make dbt-test-models MODELS=model_name`: Test specific models

## Project Architecture

### Medallion Architecture
1. **Raw Layer** (`raw` schema): Original SDE/HDE/ESI source data
2. **Staging Layer** (`staging` schema): Cleaned and normalized views with `stg_` prefix
3. **Marts Layer** (`marts` schema): Final analytical tables for consumption

### Directory Structure
- `/models/staging/`: Staging transformations (`stg_*` views)
  - `/sde/`: SDE source staging models
  - `/hde/`: HDE source staging models
- `/models/marts/`: Final analytical models (tables)
  - Universe models: regions, constellations, solar_systems
  - Infrastructure models: stargates, stations
- `/macros/`: Custom macros and tests
  - `row_count_equals`: Validates expected row counts
- `/tests/`: SQL tests for data quality
- `/analysis/`: Ad-hoc analytical queries

## Model Conventions

### Naming Standards
- **Staging models**: `stg_{source}_{entity}` (e.g., `stg_sde_map_solar_systems`)
- **Mart models**: Simple entity names (e.g., `solar_systems`, `regions`)
- **Test files**: `{model_name}.yml` alongside the SQL file

### Materialization Strategy
- **Staging**: Always use `view` (defined in dbt_project.yml)
- **Marts**: Always use `table` (defined in dbt_project.yml)
- **Seeds**: Small reference data only

### Model Development Workflow
1. Create staging model from source
2. Add schema tests in corresponding `.yml` file
3. Create mart model with business logic
4. Add row count and uniqueness tests
5. Run model and tests: `uv run dbt build --models model_name`

## Testing Standards

### Required Tests
- All primary keys must have `unique` and `not_null` tests
- All models must have `row_count_equals` test with expected count
- Foreign keys should have `relationships` tests where applicable

### Test Organization
Place tests in `{model_name}.yml` files:
```yaml
models:
  - name: model_name
    description: "Model description"
    columns:
      - name: id_column
        tests:
          - unique
          - not_null
    tests:
      - row_count_equals:
          expected_count: 10000
```

## EVE Data Domain

### Universe Hierarchy
- **Regions** (top level) → **Constellations** → **Solar Systems** (bottom level)
- Each level has unique IDs and names
- Systems connect via **Stargates** (directional connections)
- Systems contain **Stations** (player and NPC structures)

### Common Fields
- `region_id`, `constellation_id`, `solar_system_id`: Universe location IDs
- `type_id`: Item/ship/module identifier
- `group_id`, `category_id`: Item categorization
- `faction_id`, `corporation_id`: Ownership identifiers

### Data Sources
- **SDE**: Static game data (items, universe, blueprints)
- **HDE**: Hoboleaks supplemental data
- **ESI**: Live API data (prices, sovereignty, etc.)

## Development Tips

### Performance Optimization
- Use CTEs for complex transformations
- Leverage DuckDB's columnar storage
- Avoid SELECT * in production models

### Debugging
- Use `uv run dbt compile` to see compiled SQL
- Check `/target/compiled/` for generated SQL
- Use `uv run dbt test --models model_name` to test specific models
- Review `/target/run_results.json` for detailed execution info
