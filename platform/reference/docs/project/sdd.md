# System Design Document (SDD)

## Introduction

- Purpose of system: reliable automated conversion of CCP SDE into standardized outputs.
- Constraints: SDE format can change between releases; must remain reproducible and verifiable.

## High-Level Architecture

- Pipeline Ingest: pull CCP SDE release → parse raw data (YAML, SQLite, MySQL dumps).
- Transformations: apply schema mappings, curated transformations, diff generation.
- Storage: upload artifacts to Cloudflare R2 (primary distribution).
- APIs: expose metadata, diffs, and file links.
- Interfaces: SDKs, CLI, Web UI.

(Include diagram: data source → pipeline → storage → API/SDK/CLI/UI)

## Components

### Data Ingest & Normalization

- Fetch raw SDE from CCP’s official release.
- Validate integrity (checksums).
- Normalize to canonical schema.

### Conversion Pipelines

- RDBMS Exporters: Postgres, MySQL, SQLite.
- NoSQL Exporters: Mongo, Dynamo, Firestore, Redis.
- File Exporters: CSV, JSON, Parquet, YAML.
- Each exporter should be modular (pluggable interface).

### Curated Transformations

- Blueprint flattening.
- Stargate network.
- Market group hierarchy.
- Skill tree.

### Metadata & Diffs

- Maintain manifest of each version (table counts, hashes, schema info).
- Generate difference reports at table level.

### SDE Versions API

- REST API endpoints for:
- /versions - List versions
- /versions/{version} - Show details about version
- /compare/{versionA}...{versionB} - Show differences between versions

## Delivery & Distribution

- Cloudflare R2 bucket for storage and distribution.
- Signed URLs or open CDN access.
- Optional GitHub Release mirrors.

## SDKs & CLI

- SDKs in Python, TypeScript, Go (initial).
- CLI using DuckDB for local SQL queries.

## Data Model

- Canonical schema derived from CCP SDE tables.
- Mappings documented (source table → canonical → destination).
- Curated transformations as derived views.

## Non-Functional Design

- Scalability: pipeline runs in parallel across conversion modules.
- Resilience: failed conversions don’t block others.
- Testability: unit + integration tests for schema correctness.
- Observability: logs, metrics, diff reports.

## Security & Compliance

- All outputs checksum-signed.
- Public data = minimal security concerns, but integrity critical.
- Ensure compliance with CCP’s EULA/distribution policy.

## Deployment & Operations

- Data pipeline for new SDE releases.
- Automated notification (webhook, RSS, Discord bot).
- Monitoring of R2 storage and API usage.

## Open Questions

- Will the API be REST-only or also GraphQL?
- Will curated transformations be materialized (stored) or generated on-demand?
- Will NoSQL exporters be optimized loaders or just raw dumps?
