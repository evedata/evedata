# EVEData Reference Data Product

The EVEData Reference data product provides EVE reference datasets curated from the SDE (Static Data Export), ESI (EVE Swagger Interface) API, and HDE (Hoboleaks Data Export).

## Roadmap

- Core features:
  - [ ] All datasets available via Cloudflare R2
  - [ ] Data quality test suite
  - [ ] Difference reports for each table
  - [ ] API to retrieve metadata and diffs on
  - [ ] Webhook subscriptions for updates
  - [ ] Programmatic loading and updates for supported data stores
  - [ ] Indexed and non-indexed variations
  - [ ] SDKs for several languages to query the SDE programmatically
  - [ ] ORM models for popular frameworks
  - [ ] CLI to query with SQL (via DuckDB)
  - [ ] Self-contained pipelines that can be embedded in your own integration
  - [ ] Selected supplemental sources (e.g. Hoboleaks Data Export)
  - [ ] Full documentation on SDE tables and supplemental data sources
  - [ ] Curated transformations for common uses (e.g. stargate network)
  - [ ] Web UI to browse table data
- Supported destinations:
  - [ ] MySQL (including MariaDB)
  - [ ] PostgreSQL
  - [ ] SQLite
  - [ ] SQL Server
  - [ ] CSV
  - [ ] JSON
  - [ ] Parquet
  - [ ] YAML
