FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

RUN uv python install 3.13

WORKDIR /evedata

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    # --mount=type=bind,source=docs/pyproject.toml,target=docs/pyproject.toml \
    # --mount=type=bind,source=infra/pyproject.toml,target=infra/pyproject.toml \
    # --mount=type=bind,source=platform/admin/pyproject.toml,target=platform/admin/pyproject.toml \
    # --mount=type=bind,source=platform/admin-core/pyproject.toml,target=platform/admin-core/pyproject.toml \
    # --mount=type=bind,source=platform/core/pyproject.toml,target=platform/core/pyproject.toml \
    # --mount=type=bind,source=platform/datasets/pyproject.toml,target=platform/datasets/pyproject.toml \
    # --mount=type=bind,source=platform/rest/pyproject.toml,target=platform/rest/pyproject.toml \
    # --mount=type=bind,source=platform/rest-core/pyproject.toml,target=platform/rest-core/pyproject.toml \
    # --mount=type=bind,source=platform/static/pyproject.toml,target=platform/static/pyproject.toml \
    # --mount=type=bind,source=platform/transformations/pyproject.toml,target=platform/transformations/pyproject.toml \
    # --mount=type=bind,source=platform/utils/pyproject.toml,target=platform/utils/pyproject.toml \
    uv sync --frozen --no-install-workspace --no-dev
COPY . /evedata
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --all-packages --no-dev
RUN uv run dbt deps

FROM debian:bookworm-slim

COPY --from=builder --chown=python:python /python /python
COPY --from=builder --chown=app:app /evedata /evedata

ENV PATH="/evedata/.venv/bin:$PATH"

ENV EVEDATA_HOME=/evedata

CMD ["evedatactl", "--help"]
