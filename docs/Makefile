build-pr: clean pip-requirements
	rm -f mkdocs.pr.yml
	echo "INHERIT: ./mkdocs.yml" > mkdocs.pr.yml
	echo "site_name: EVEData Documentation (PR-${PR_NUMBER})" >> mkdocs.pr.yml
	echo "site_url: https://pr-${PR_NUMBER}-evedata-docs-dev.evedata-dqt.workers.dev" >> mkdocs.pr.yml
	uv run mkdocs build --config-file mkdocs.pr.yml
	echo "User-Agent: *\nDisallow: /" > site/robots.txt

build-stg: clean pip-requirements
	uv run mkdocs build --config-file mkdocs.stg.yml
	echo "User-Agent: *\nDisallow: /" > site/robots.txt

build-prd: clean pip-requirements
	EVEDATA_DOCS_ENV=prd uv run mkdocs build --strict

clean:
	rm -rf dist site .cache

deploy-pr: build-pr
	pnpm run deploy:pr

deploy-stg: build-stg
	pnpm run deploy:stg

deploy-prd: build-prd
	pnpm run deploy:prd

dev:
	uv run mkdocs serve -a localhost:8080

fix: fix-markdown

fix-markdown:
	pnpm run fix:markdown

lint: lint-markdown

lint-markdown:
	pnpm run lint:markdown

pip-requirements:
	uv pip freeze > requirements.txt
