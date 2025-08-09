# CLAUDE.md

This workspace member contains the documentation site for EVEData.

## Organization

- @docs: Root directory for documentation site content source files
- @includes: Markdown files that are appended to every page (MUST be listed in `pymdownx.snippets.auto_append` setting in @mkdocs.yml)
- @overrides/partials: MkDocs Material [partial overrides](https://squidfunk.github.io/mkdocs-material/customization/#overriding-partials)
- @overrides/main.html: MkDocs Material [block overrides](https://squidfunk.github.io/mkdocs-material/customization/#overriding-blocks)
- @references: Reference materials not included in documentation site.

## Key features

- [MkDocs Material][mkdocs-material]
- Hosted as an asset-only site on [Cloudflare Workers][cloudflare-workers]
- Deployed from the [evedata/evedata](https://github.com/evedata/evedata) monorepo with GitHub Actions (@../.github/workflows/docs.yml) and Wrangler (@wrangler.toml)
- PR preview URLs: `pr-<number>-evedata-dev.evedata-dqt.workers.dev`
- Staging URL: [docs-stg.evedata.dev](https://docs-stg.evedata.dev)
- Production URL: [docs.evedata.io](https://docs.evedata.io)

## Tools

- `make build`: Build the site.
- `make build-prd`: Build the site for production.
- `make clean`: Remove build artifacts.
- `make deploy-stg`: Build and deploy to staging.
- `make deploy-prd`: Build and deploy to production.
- `make fix`: Auto-fix Markdown linting errors.
- `make lint`: Lint Markdown with [Markdownlint][markdownlint].

[cloudflare-workers]: https://developers.cloudflare.com/workers/
[markdownlint]: https://github.com/DavidAnson/markdownlint
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
