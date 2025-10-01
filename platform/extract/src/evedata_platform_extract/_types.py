from typing import TYPE_CHECKING, Any, NotRequired, TypedDict

if TYPE_CHECKING:
    from collections.abc import Callable

    from dlt.common.schema.typing import (
        TAnySchemaColumns,
        TFileFormat,
        TSchemaContract,
        TTableFormat,
        TTableReferenceParam,
        TWriteDispositionConfig,
    )
    from dlt.common.typing import TColumnNames, TTableHintTemplate, TTableNames
    from dlt.extract.hints import TResourceNestedHints
    from dlt.extract.incremental import TIncrementalConfig


class ResourceHints(TypedDict, total=False):
    """Represents schema hints for a DLT resource."""

    table_name: "TTableHintTemplate[str]"
    parent_table_name: "TTableHintTemplate[str]"
    write_disposition: "TTableHintTemplate[TWriteDispositionConfig]"
    columns: "TTableHintTemplate[TAnySchemaColumns]"
    primary_key: "TTableHintTemplate[TColumnNames]"
    merge_key: "TTableHintTemplate[TColumnNames]"
    incremental: "TIncrementalConfig"
    schema_contract: "TTableHintTemplate[TSchemaContract]"
    additional_table_hints: dict[str, "TTableHintTemplate[Any]"] | None
    table_format: "TTableHintTemplate[TTableFormat]"
    file_format: "TTableHintTemplate[TFileFormat]"
    references: "TTableHintTemplate[TTableReferenceParam]"
    create_table_variant: bool
    nested_hints: "TTableHintTemplate[dict[TTableNames, TResourceNestedHints]]"


class ResourceConfig(TypedDict):
    hints: NotRequired["ResourceHints"]
    name_from_inv_names: NotRequired[bool]
    rename_columns: NotRequired[dict[str, str]]
    before_extract: NotRequired[list["Callable[[dict[str, Any]], dict[str, Any]]"]]
    before_load: NotRequired[list["Callable[[dict[str, Any]], dict[str, Any]]"]]


class FileResourceConfig(ResourceConfig):
    pass


class GlobResourceConfig(FileResourceConfig):
    glob: str


class ESIResourceConfig(ResourceConfig):
    path: str
    ids_path: NotRequired[str | None]
    include_id_in_record: NotRequired[bool | None]
    depends_on: NotRequired[str]
    ids_fn: NotRequired["Callable[[dict[str, Any], ESIResourceConfig], list[int]]"]
