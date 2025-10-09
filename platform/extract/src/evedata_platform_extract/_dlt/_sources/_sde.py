from typing import TYPE_CHECKING, Any

import dlt
from dlt.sources.filesystem import filesystem, read_jsonl

if TYPE_CHECKING:
    from pathlib import Path

    from dlt.extract import DltResource


@dlt.source
def sde(path: "Path", version: int) -> Any:
    """A DLT source for the EVE Online Static Data Export (SDE)."""
    resources: list[DltResource] = []
    for sde_file in path.glob("*.jsonl"):
        if sde_file.stem == "_sde":
            continue

        file = filesystem(bucket_url=f"file:/{sde_file}", file_glob="") | read_jsonl()
        file = file.with_name(sde_file.stem)
        file = file.apply_hints(write_disposition="append")
        file = file.add_map(lambda r: r | {"_sde_version": version})

        resources.append(file)

    yield from resources
