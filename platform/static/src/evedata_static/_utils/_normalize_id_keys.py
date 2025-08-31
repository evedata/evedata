"""Normalize dictionary keys used as IDs in EVE SDE data.

This module provides functionality to transform EVE Online's Static Data Export (SDE)
YAML structures and Hoboleaks Data Export (HDE) JSON structures into normalized formats,
primarily converting dictionaries that use their keys as IDs into lists of dictionaries
with explicit 'id' fields.
"""

from functools import lru_cache
from typing import TYPE_CHECKING, Any, cast, overload

from evedata_utils.json import load_json_file
from evedata_utils.yaml import load_yaml_file

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path


class NormalizationError(Exception):
    """Exception raised when data normalization fails.

    This exception wraps various error conditions that can occur during normalization,
    including unsupported data structures, mixed types, and recursion depth exceeded.
    """

    def __init__(
        self, message: str, *, data: Any = None, cause: Exception | None = None
    ) -> None:
        """Initialize NormalizationError with context.

        Args:
            message: Error description
            data: The data that caused the error (optional)
            cause: The underlying exception that caused this error (optional)
        """
        super().__init__(message)
        self.data = data
        self.cause = cause
        if cause:
            self.__cause__ = cause


type ScalarType = bool | int | float | str
type IdKeyType = int | str
type NormalizedDict = dict[str, Any]
type NormalizedList = list[NormalizedDict]
type NormalizedData = NormalizedList | NormalizedDict | ScalarType | list[Any]

type InputDictType = (
    dict[int, NormalizedDict]
    | dict[int, list[NormalizedDict]]
    | dict[int, ScalarType | list[ScalarType]]
    | dict[str, Any]
    | dict[str, NormalizedDict]
)
type InputType = InputDictType | NormalizedList | ScalarType | list[Any]


@lru_cache(maxsize=128)
def _is_int(value: str) -> bool:
    """Check if a string can be converted to an integer.

    Results are cached to improve performance for repeated checks.
    """
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


def _is_int_like_key(key: Any) -> bool:
    """Check if a key is an integer or integer-like string."""
    if isinstance(key, int):
        return True
    if isinstance(key, str):
        return _is_int(key)
    return False


def _has_all_int_like_keys(data: dict[Any, Any]) -> bool:
    """Check if all dictionary keys are integer-like."""
    return all(_is_int_like_key(k) for k in data)


def _has_all_string_keys(data: dict[Any, Any]) -> bool:
    """Check if all dictionary keys are strings."""
    return all(isinstance(k, str) for k in data)


def _all_values_are_scalars(data: dict[Any, Any]) -> bool:
    """Check if all values are scalar types (not dict)."""
    return all(not isinstance(v, dict) for v in data.values())


def _all_list_items_are_dicts(lst: list[Any]) -> bool:
    """Check if all list items are dictionaries."""
    return all(isinstance(item, dict) for item in lst)


def _all_list_items_are_scalars(lst: list[Any]) -> bool:
    """Check if all list items are scalar values."""
    return all(not isinstance(item, dict) for item in lst)


@overload
def normalize_id_keys(
    data: dict[int, NormalizedDict],
    *,
    _depth: int = 0,
    _max_depth: int = 100,
) -> NormalizedList | NormalizedDict: ...


@overload
def normalize_id_keys(
    data: dict[int, list[NormalizedDict]],
    *,
    _depth: int = 0,
    _max_depth: int = 100,
) -> NormalizedList: ...


@overload
def normalize_id_keys(
    data: dict[int, ScalarType | list[ScalarType]],
    *,
    _depth: int = 0,
    _max_depth: int = 100,
) -> dict[str, ScalarType | list[ScalarType]]: ...


@overload
def normalize_id_keys(
    data: dict[str, Any],
    *,
    _depth: int = 0,
    _max_depth: int = 100,
) -> NormalizedDict: ...


@overload
def normalize_id_keys(
    data: NormalizedList,
    *,
    _depth: int = 0,
    _max_depth: int = 100,
) -> NormalizedList: ...


@overload
def normalize_id_keys(
    data: ScalarType | list[Any],
    *,
    _depth: int = 0,
    _max_depth: int = 100,
) -> NormalizedList | list[Any]: ...


def normalize_id_keys(  # noqa: PLR0911
    data: InputType,
    *,
    _depth: int = 0,
    _max_depth: int = 100,
) -> NormalizedData:
    """Normalize dictionary keys used as IDs in EVE SDE data.

    This function transforms various data structures from EVE Online's Static Data
    Export (SDE) YAML files into a normalized format. The primary transformation
    is converting dictionaries that use their keys as IDs into lists of dictionaries
    with explicit 'id' fields.

    Transformation Rules:
        1. Scalars (bool, int, float, str) -> unchanged
        2. Lists of scalars -> unchanged
        3. Lists of dicts -> each dict normalized recursively
        4. Dict with int-like keys and scalar values
            -> list of {"id": key, "value": val}
        5. Dict with int-like keys and dict values
            -> list of {"id": key, **normalized_val}
        6. Dict with string keys -> values normalized recursively
        7. Empty dict -> empty list

    Args:
        data: Input data structure to normalize. Can be:
            - Scalar values (bool, int, float, str)
            - Lists (homogeneous preferred)
            - Dictionaries with various key/value types
        _depth: Internal recursion depth tracking (do not use)
        _max_depth: Maximum recursion depth (default: 100)

    Returns:
        Normalized data structure. The type depends on input:
        - Scalars return unchanged
        - ID-keyed dicts return lists
        - String-keyed dicts return dicts
        - Lists return lists

    Raises:
        NormalizationError: If data structure cannot be normalized (e.g., mixed list
            types, mixed dict key types, unsupported data types, or maximum recursion
            depth exceeded)

    Examples:
        Basic ID normalization:
        >>> normalize_id_keys({1: {"name": "Rifter"}, 2: {"name": "Slasher"}})
        [{"id": 1, "name": "Rifter"}, {"id": 2, "name": "Slasher"}]

        String keys preserved:
        >>> normalize_id_keys({"ships": {"frigate": "small"}})
        {"ships": {"frigate": "small"}}

        ID keys with scalar values:
        >>> normalize_id_keys({1: "value1", 2: "value2"})
        [{"id": 1, "value": "value1"}, {"id": 2, "value": "value2"}]
    """
    if _depth > _max_depth:
        msg = f"Maximum recursion depth ({_max_depth}) exceeded"
        raise NormalizationError(msg, data=data, cause=RecursionError(msg))

    if isinstance(data, bool | int | float | str):
        return data

    if isinstance(data, list):
        if _all_list_items_are_scalars(data):
            return data

        if _all_list_items_are_dicts(data):
            return [
                normalize_id_keys(item, _depth=_depth + 1, _max_depth=_max_depth)
                for item in data
            ]

        dict_count = sum(1 for item in data if isinstance(item, dict))
        non_dict_count = len(data) - dict_count
        msg = (
            f"Cannot normalize list with mixed types: {dict_count} dict(s) and"
            f" {non_dict_count} non-dict item(s)"
        )
        raise NormalizationError(msg, data=data)

    if isinstance(data, dict):  # pyright: ignore[reportUnnecessaryIsInstance]
        if not data:
            return []

        if _has_all_int_like_keys(data):
            if _all_values_are_scalars(data):
                return [{"id": int(k), "value": v} for k, v in data.items()]

            try:
                return [
                    {
                        "id": int(k),
                        **cast(
                            "dict[str, Any]",
                            normalize_id_keys(
                                v, _depth=_depth + 1, _max_depth=_max_depth
                            ),
                        ),
                    }
                    for k, v in data.items()
                ]
            except (ValueError, TypeError) as e:
                msg = f"Failed to normalize dict values: {e}"
                raise NormalizationError(msg, data=data, cause=e) from e

        if _has_all_string_keys(data):
            try:
                return {
                    str(k): normalize_id_keys(
                        v, _depth=_depth + 1, _max_depth=_max_depth
                    )
                    for k, v in data.items()
                }
            except (ValueError, TypeError) as e:
                msg = f"Failed to normalize dict values: {e}"
                raise NormalizationError(msg, data=data, cause=e) from e

    max_sample_len = 100
    sample = (
        str(data)[:max_sample_len] + "..."
        if len(str(data)) > max_sample_len
        else str(data)
    )
    msg = (
        f"Cannot normalize data structure of type {type(data).__name__}."
        f" Sample: {sample}"
    )
    raise NormalizationError(msg, data=data)


def load_json_with_normalized_id_keys(
    path: "str | Path",
) -> "Generator[dict[str, Any]]":
    data = load_json_file(path)
    if isinstance(data, list) and all(
        isinstance(item, bool | float | int | str) for item in data
    ):
        for item in data:
            yield {"value": item}
    elif isinstance(data, list):
        for item in data:
            yield cast("NormalizedDict", normalize_id_keys(item))
    elif all(isinstance(v, bool | float | int | str) for v in data.values()):
        for k, v in data.items():
            yield cast("dict[str, Any]", {"key": k, "value": v})
    elif all(_is_int(k) and not isinstance(v, dict) for k, v in data.items()):
        for id_, value in data.items():
            yield {"id": int(id_), "value": value}
    elif all(_is_int(k) for k in data):
        for id_, item in data.items():
            yield {"id": int(id_), **cast("NormalizedDict", normalize_id_keys(item))}
    else:
        yield normalize_id_keys(data)


def load_yaml_with_normalized_id_keys(
    path: "str | Path",
) -> "Generator[dict[str, Any]]":
    data: dict[int, dict[str, Any]] | dict[str, Any] | list[dict[str, Any]] = (
        load_yaml_file(path)
    )
    if isinstance(data, list) and all(
        isinstance(item, bool | float | int | str) for item in data
    ):
        for item in data:
            yield {"value": item}
    if isinstance(data, list):
        for item in data:
            yield normalize_id_keys(item)
    elif all(
        isinstance(k, str) and isinstance(v, bool | float | int | str)
        for k, v in data.items()
    ):
        for k, v in data.items():
            yield cast("dict[str, Any]", {"key": k, "value": v})
    elif all(isinstance(k, str) for k in data):
        yield cast("dict[str, Any]", normalize_id_keys(data))
    else:
        for id_, item in data.items():
            yield {"id": id_, **normalize_id_keys(item)}
