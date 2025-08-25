# Product Requirements Document (PRD)

## Executive Summary

- Brief description of EVE Static (purpose, audience, value).
- High-level problem statement: difficulty of using raw CCP SDE data directly.
- Vision: make the SDE, HDE, and ESI reference data universally accessible in structured, queryable, and developer-friendly forms.

## Goals & Objectives

- Provide clean, standardized exports of the SDE, HDE, and ESI reference data in multiple formats.
- Enable developers, data scientists, and EVE players to build tools quickly.
- Ensure accuracy, versioning, and reproducibility of SDE datasets.
- Establish foundation for future integrations (SDKs, pipelines, curated transformations).

## Scope

- In Scope: conversions with curated schema, API access, SDKs, CLI, curated transformations, diff reports.
- Out of Scope: dynamic ESI data, in-game telemetry.

## Target Users

- Tool developers (e.g. fitting tools, market tools, corp dashboards).
- Data scientists / analysts doing research on EVE economy or geography.
- EVE enthusiasts wanting lightweight local queries.

## User Stories

- “As a developer, I want a Postgres dump of the SDE so I can run queries in my backend.”
- “As an analyst, I want a Parquet export so I can analyze with Pandas.”
- “As a tool maintainer, I want an SDK so I can fetch diffs without rebuilding the pipeline.”
- “As a player, I want a CLI with SQL support so I can explore item data quickly.”
- "As a player, I want an MCP server so I can explore item data with natural language."

## Functional Requirements

- Conversions to RDBMS, NoSQL, and file formats.
- Metadata/diff API with versioning.
- Webhook subscriptions for updates.
- Curated, normalized schema
- Curated transformations (blueprints, stargate networks, etc.).
- Documentation of tables and supplemental data.

## Non-Functional Requirements

- Performance: scalable to large SDE dumps (GBs).
- Reliability: accurate, repeatable, versioned outputs.
- Availability: hosted via Cloudflare R2 + CDN.
- Security: open/public access, but with integrity checks (hashes).
- Extensibility: easily add new formats/destinations.

## Success Metrics

- Adoption: number of downloads or API calls.
- Coverage: # of supported formats/destinations.
- Accuracy: no mismatches between raw SDE and converted data (via test suite).
- Developer satisfaction: SDK/CLI usage, community contributions.

## Risks & Mitigations

- Scope creep → phased roadmap.
- Upstream changes in SDE format → modular pipeline.
- Storage costs → efficient compression, caching.
- Data misinterpretation → curated docs & tests.

## Roadmap & Milestones

- Phase 1: Core conversions + API + CLI + docs.
- Phase 2: SDKs, curated transformations, web UI.
- Phase 3: NoSQL destinations, supplemental sources.
- Phase 4: Advanced features (ORMs, pipelines).
