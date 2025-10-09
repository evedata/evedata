import time
from typing import TYPE_CHECKING, Any, cast

import pytest

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

from evedata_platform_static._utils._normalize_id_keys import (
    NormalizationError,
    _is_int,  # pyright: ignore[reportPrivateUsage]
    _is_int_like_key,  # pyright: ignore[reportPrivateUsage]
    normalize_id_keys,
)


class TestScalarInputs:
    @pytest.mark.parametrize(
        "value",
        [
            True,
            False,
            42,
            3.14,
            0,
            -1,
            float("inf"),
            "test",
            "",
            "123",
            "with spaces",
        ],
    )
    def test_scalar_values_unchanged(self, value: Any):
        result = normalize_id_keys(value)
        if isinstance(value, bool):
            # booleans must be same object, not just equal
            assert result is value
        else:
            assert result == value


class TestListInputs:
    def test_list_of_scalars(self):
        assert normalize_id_keys([1, 2, 3]) == [1, 2, 3]
        assert normalize_id_keys(["a", "b", "c"]) == ["a", "b", "c"]
        assert normalize_id_keys([True, False]) == [True, False]
        assert normalize_id_keys([1, "mixed", 3.14]) == [1, "mixed", 3.14]

    def test_empty_list(self):
        assert normalize_id_keys([]) == []

    def test_list_of_dicts(self):
        input_data = [{"name": "test"}, {"_key": 1}]
        expected = [{"name": "test"}, {"_key": 1}]
        assert normalize_id_keys(input_data) == expected

    def test_list_of_dicts_with_nested_normalization(self):
        input_data = [{"key": {1: {"value": "test"}}}]
        expected = [{"key": [{"_key": 1, "value": "test"}]}]
        assert normalize_id_keys(input_data) == expected

    def test_mixed_list_with_dicts(self):
        # Lists with mixed types where some are dicts should trigger NormalizationError
        with pytest.raises(
            NormalizationError, match="Cannot normalize list with mixed types"
        ):
            normalize_id_keys([1, {"key": "value"}, "string"])


class TestIntKeyedDicts:
    def test_dict_int_keys_scalar_values(self):
        input_data: dict[int, str] = {1: "a", 2: "b", 3: "c"}
        expected = [
            {"_key": 1, "value": "a"},
            {"_key": 2, "value": "b"},
            {"_key": 3, "value": "c"},
        ]
        result = cast(
            "list[dict[str, Any]]", normalize_id_keys(cast("Any", input_data))
        )
        assert sorted(result, key=lambda x: x["_key"]) == sorted(
            expected, key=lambda x: x["_key"]
        )

    def test_dict_string_int_keys_scalar_values(self):
        input_data = {"1": "a", "2": "b", "3": "c"}
        expected = [
            {"_key": 1, "value": "a"},
            {"_key": 2, "value": "b"},
            {"_key": 3, "value": "c"},
        ]
        result = cast("list[dict[str, Any]]", normalize_id_keys(input_data))
        assert sorted(result, key=lambda x: x["_key"]) == sorted(
            expected, key=lambda x: x["_key"]
        )

    def test_dict_mixed_int_string_keys_scalar_values(self):
        input_data: dict[int | str, str] = {1: "a", "2": "b", 3: "c"}
        expected = [
            {"_key": 1, "value": "a"},
            {"_key": 2, "value": "b"},
            {"_key": 3, "value": "c"},
        ]
        result = cast(
            "list[dict[str, Any]]", normalize_id_keys(cast("Any", input_data))
        )
        assert sorted(result, key=lambda x: x["_key"]) == sorted(
            expected, key=lambda x: x["_key"]
        )

    def test_dict_int_keys_dict_values(self):
        input_data = {1: {"name": "test1"}, 2: {"name": "test2"}}
        expected = [{"_key": 1, "name": "test1"}, {"_key": 2, "name": "test2"}]
        result = cast("list[dict[str, Any]]", normalize_id_keys(input_data))
        assert sorted(result, key=lambda x: x["_key"]) == sorted(
            expected, key=lambda x: x["_key"]
        )

    def test_dict_int_keys_list_values(self):
        input_data: dict[int, list[str]] = {1: ["a", "b"], 2: ["c", "d"]}
        expected = [{"_key": 1, "value": ["a", "b"]}, {"_key": 2, "value": ["c", "d"]}]
        result = cast(
            "list[dict[str, Any]]", normalize_id_keys(cast("Any", input_data))
        )
        assert sorted(result, key=lambda x: x["_key"]) == sorted(
            expected, key=lambda x: x["_key"]
        )

    def test_dict_int_keys_with_nested_dict(self):
        input_data = {
            1: {"name": "item1", "props": {"color": "red"}},
            2: {"name": "item2", "props": {"color": "blue"}},
        }
        expected = [
            {"_key": 1, "name": "item1", "props": {"color": "red"}},
            {"_key": 2, "name": "item2", "props": {"color": "blue"}},
        ]
        result = cast("list[dict[str, Any]]", normalize_id_keys(input_data))
        assert sorted(result, key=lambda x: cast("int", x["_key"])) == sorted(
            expected, key=lambda x: cast("int", x["_key"])
        )


class TestStringKeyedDicts:
    def test_dict_string_keys_scalar_values(self):
        input_data = {"key1": "value1", "key2": "value2"}
        expected = {"key1": "value1", "key2": "value2"}
        assert normalize_id_keys(input_data) == expected

    def test_dict_string_keys_dict_values(self):
        input_data = {"parent": {"child": "value"}}
        expected = {"parent": {"child": "value"}}
        assert normalize_id_keys(input_data) == expected

    def test_dict_string_keys_mixed_values(self):
        input_data = {
            "str": "value",
            "num": 42,
            "list": [1, 2],
            "dict": {"nested": "value"},
        }
        expected = {
            "str": "value",
            "num": 42,
            "list": [1, 2],
            "dict": {"nested": "value"},
        }
        assert normalize_id_keys(input_data) == expected

    def test_dict_string_keys_with_int_like_dict_values(self):
        input_data = {"parent": {1: "value1", 2: "value2"}}
        expected = {
            "parent": [{"_key": 1, "value": "value1"}, {"_key": 2, "value": "value2"}]
        }
        result = normalize_id_keys(input_data)
        assert isinstance(result, dict)
        if isinstance(result["parent"], list):
            result_parent: list[dict[str, Any]] = result["parent"]  # type: ignore[assignment]
            expected_parent: list[dict[str, Any]] = expected["parent"]  # type: ignore[assignment]
            result["parent"] = sorted(result_parent, key=lambda x: x["_key"])
            expected["parent"] = sorted(expected_parent, key=lambda x: x["_key"])
        assert result == expected


class TestNestedStructures:
    def test_parent_child_structure(self):
        input_data = {
            1: [{"name": "child1"}, {"name": "child2"}],
            2: [{"name": "child3"}],
        }
        # Doesn't match parentID flattening pattern
        expected = [
            {"_key": 1, "value": [{"name": "child1"}, {"name": "child2"}]},
            {"_key": 2, "value": [{"name": "child3"}]},
        ]
        result = cast(
            "list[dict[str, Any]]", normalize_id_keys(cast("Any", input_data))
        )
        # Sort by id for consistent comparison
        result_sorted = sorted(result, key=lambda x: x["_key"])
        expected_sorted = sorted(expected, key=lambda x: x["_key"])
        assert result_sorted == expected_sorted

    def test_deeply_nested_structure(self):
        input_data = {
            1: [
                {"type": "A", "data": {10: {"value": "x"}}},
                {"type": "B", "data": {20: {"value": "y"}}},
            ],
            2: [{"type": "C", "data": {30: {"value": "z"}}}],
        }
        # List values containing dicts aren't recursively normalized
        expected = [
            {
                "_key": 1,
                "value": [
                    {"type": "A", "data": {10: {"value": "x"}}},
                    {"type": "B", "data": {20: {"value": "y"}}},
                ],
            },
            {"_key": 2, "value": [{"type": "C", "data": {30: {"value": "z"}}}]},
        ]
        result = cast(
            "list[dict[str, Any]]", normalize_id_keys(cast("Any", input_data))
        )
        # Sort for consistent comparison
        result_sorted = sorted(result, key=lambda x: x["_key"])
        expected_sorted = sorted(expected, key=lambda x: x["_key"])
        assert result_sorted == expected_sorted

    def test_complex_nested_with_mixed_types(self):
        input_data = {
            100: [
                {
                    "name": "item1",
                    "materials": {1: 10, 2: 20},
                    "skills": ["skill1", "skill2"],
                }
            ]
        }
        # List values with dicts aren't recursively normalized
        expected = [
            {
                "_key": 100,
                "value": [
                    {
                        "name": "item1",
                        "materials": {1: 10, 2: 20},
                        "skills": ["skill1", "skill2"],
                    }
                ],
            }
        ]
        result = cast(
            "list[dict[str, Any]]", normalize_id_keys(cast("Any", input_data))
        )
        assert result == expected


class TestEdgeCases:
    def test_empty_dict(self):
        # Empty dict becomes empty list for consistency with ID-keyed dict behavior
        assert normalize_id_keys({}) == []

    def test_none_values_in_dict(self):
        # None values in string-keyed dicts trigger error during recursive normalization
        with pytest.raises(
            NormalizationError, match="Cannot normalize data structure of type NoneType"
        ):
            normalize_id_keys({"key": None})

        # None values in int-keyed dicts are preserved as scalars
        assert normalize_id_keys(cast("Any", {1: None})) == [{"_key": 1, "value": None}]

    def test_very_large_integers(self):
        large_int = 999999999999999
        input_data: dict[int, str] = {large_int: "value"}
        expected = [{"_key": 999999999999999, "value": "value"}]
        assert normalize_id_keys(cast("Any", input_data)) == expected

        input_data2 = {"999999999999999": "value"}
        expected2 = [{"_key": 999999999999999, "value": "value"}]
        assert normalize_id_keys(input_data2) == expected2

    def test_unicode_keys(self):
        input_data = {"日本語": "value", "emoji😀": "test"}
        expected = {"日本語": "value", "emoji😀": "test"}
        assert normalize_id_keys(input_data) == expected

    def test_special_string_keys(self):
        input_data = {"__proto__": "value1", "constructor": "value2"}
        expected = {"__proto__": "value1", "constructor": "value2"}
        assert normalize_id_keys(input_data) == expected

    def test_negative_integer_keys(self):
        input_data: dict[int, str] = {-1: "negative", -100: "very negative"}
        expected = [
            {"_key": -1, "value": "negative"},
            {"_key": -100, "value": "very negative"},
        ]
        result = cast(
            "list[dict[str, Any]]", normalize_id_keys(cast("Any", input_data))
        )
        assert sorted(result, key=lambda x: x["_key"]) == sorted(
            expected, key=lambda x: x["_key"]
        )

    def test_zero_as_key(self):
        input_data: dict[int, str] = {0: "zero value"}
        expected = [{"_key": 0, "value": "zero value"}]
        assert normalize_id_keys(cast("Any", input_data)) == expected


class TestErrorConditions:
    def test_unsupported_structure_mixed_dict_keys(self):
        with pytest.raises(NormalizationError, match="Cannot normalize data structure"):
            normalize_id_keys(cast("Any", {1: "int", "str": "string"}))

    def test_mixed_list_types(self):
        with pytest.raises(
            NormalizationError, match="Cannot normalize list with mixed types"
        ):
            normalize_id_keys([{"key": "value"}, "string", 123])


class TestEVEDataIntegration:
    def test_eve_type_ids_structure(self):
        input_data = {
            587: {
                "name": {"en": "Rifter"},
                "groupID": 25,
                "mass": 1067000.0,
                "volume": 27289.0,
            },
            588: {
                "name": {"en": "Slasher"},
                "groupID": 25,
                "mass": 1030000.0,
                "volume": 13900.0,
            },
        }

        result = normalize_id_keys(input_data)
        assert isinstance(result, list)
        assert len(result) == 2

        for item in result:
            assert "_key" in item
            assert "name" in item
            assert "groupID" in item
            assert "mass" in item
            assert "volume" in item

    def test_eve_blueprints_structure(self):
        input_data = {
            681: {
                "blueprintTypeID": 681,
                "activities": {
                    "manufacturing": {
                        "materials": {34: 11000, 35: 2200},
                        "products": {582: 1},
                        "time": 600,
                    }
                },
            }
        }

        result = normalize_id_keys(input_data)
        assert isinstance(result, list)
        assert len(result) == 1

        blueprint = result[0]
        assert blueprint["_key"] == 681
        assert "activities" in blueprint
        assert "manufacturing" in blueprint["activities"]

        materials = blueprint["activities"]["manufacturing"]["materials"]
        expected_materials = [{"_key": 34, "value": 11000}, {"_key": 35, "value": 2200}]
        assert sorted(materials, key=lambda x: x["_key"]) == sorted(
            expected_materials, key=lambda x: x["_key"]
        )

    def test_eve_market_groups_structure(self):
        input_data = {
            4: {"nameID": {"en": "Ships"}, "parentGroupID": None, "iconID": 3},
            5: {"nameID": {"en": "Frigates"}, "parentGroupID": 4, "iconID": 3},
        }

        # None values would cause error, use 0 instead
        input_data[4]["parentGroupID"] = 0

        result = normalize_id_keys(input_data)
        assert isinstance(result, list)
        assert len(result) == 2

        for group in result:
            assert "_key" in group
            assert "nameID" in group

    def test_realistic_nested_eve_data(self):
        input_data = {
            "types": {
                587: {"name": "Rifter", "group": 25},
                588: {"name": "Slasher", "group": 25},
            },
            "groups": {25: {"name": "Frigate", "category": 6}},
            "categories": {6: {"name": "Ship"}},
        }

        result = normalize_id_keys(input_data)
        assert isinstance(result, dict)
        assert "types" in result
        assert "groups" in result
        assert "categories" in result

        assert isinstance(result["types"], list)
        assert isinstance(result["groups"], list)
        assert isinstance(result["categories"], list)


class TestPerformance:
    def test_large_dataset_performance(self):
        # Create dict with 10,000 entries
        large_data = {i: {"value": f"item_{i}"} for i in range(10000)}

        start = time.perf_counter()
        result = normalize_id_keys(large_data)
        elapsed = time.perf_counter() - start

        # Should complete in reasonable time (< 1 second)
        assert elapsed < 1.0
        assert len(result) == 10000
        assert all("_key" in item for item in result)

    def test_deep_nesting_performance(self):
        # Create deeply nested structure
        def create_nested(depth: int) -> dict[str, Any]:
            if depth == 0:
                return {"value": "leaf"}
            return {"nested": create_nested(depth - 1)}

        deep_data = create_nested(50)
        result = normalize_id_keys(deep_data)
        current = result
        for _ in range(50):
            assert "nested" in current
            current = current["nested"]
        assert current == {"value": "leaf"}


class TestTypePreservation:
    def test_return_type_consistency(self):
        # Test that return types match expected patterns

        # Scalar inputs return same type
        assert type(normalize_id_keys(42)) is int
        assert type(normalize_id_keys(3.14)) is float
        assert type(normalize_id_keys("test")) is str
        assert type(normalize_id_keys(True)) is bool  # noqa: FBT003

        # List of scalars returns list
        assert type(normalize_id_keys([1, 2, 3])) is list

        # Dict with string keys returns dict
        assert type(normalize_id_keys({"key": "value"})) is dict

        # Dict with int keys returns list
        assert type(normalize_id_keys({1: {"key": "value"}})) is list

    def test_preserve_value_types(self):
        # Ensure value types are preserved through transformation
        # Note: None values cause ValueError, so we'll exclude them
        input_data = {
            1: {
                "string": "text",
                "int": 42,
                "float": 3.14,
                "bool": True,
                "list": [1, 2, 3],
            }
        }

        result = cast("list[dict[str, Any]]", normalize_id_keys(input_data))
        item = result[0]

        assert type(item["string"]) is str
        assert type(item["int"]) is int
        assert type(item["float"]) is float
        assert type(item["bool"]) is bool
        assert type(item["list"]) is list


class TestHelperFunctions:
    @pytest.mark.parametrize(
        "value",
        [
            "123",
            "0",
            "-456",
            "999999",
            "-999999",
            "+123",
            "00123",
            "-0",
            "+0",
        ],
    )
    def test_valid_integers(self, value: str):
        assert _is_int(value) is True

    @pytest.mark.parametrize(
        "value",
        [
            "12.3",
            "abc",
            "",
            "12a",
            "1.0",
            " ",
            "1 2",
            "1e5",
        ],
    )
    def test_invalid_integers(self, value: str):
        assert _is_int(value) is False

    def test_is_int_like_key_returns_false(self):
        assert _is_int_like_key("not_a_number") is False
        assert _is_int_like_key("12.34") is False
        assert _is_int_like_key("") is False
        assert _is_int_like_key(None) is False
        assert _is_int_like_key([]) is False
        assert _is_int_like_key({}) is False
        assert _is_int_like_key(3.14) is False


class TestNormalizationError:
    def test_normalization_error_with_cause(self):
        original_error = ValueError("Original error")
        error = NormalizationError(
            "Test error", data={"test": "data"}, cause=original_error
        )

        assert error.__cause__ is original_error
        assert error.data == {"test": "data"}
        assert error.cause is original_error
        assert str(error) == "Test error"


class TestRecursionAndMocking:
    def test_recursive_calls_tracked(self, mocker: "MockerFixture"):
        import evedata_platform_static._utils._normalize_id_keys as module  # noqa: PLC0415

        spy = mocker.spy(module, "normalize_id_keys")
        data = {"key1": {"nested": "value"}, "key2": [{"item": 1}]}
        result = normalize_id_keys(data)

        # Expect 5 calls: main + 2 dict values + nested string + list item
        assert spy.call_count == 5
        assert result == {"key1": {"nested": "value"}, "key2": [{"item": 1}]}

    def test_recursion_depth_exceeded(self):
        data = {"nested": {"deeper": {"deepest": "value"}}}

        with pytest.raises(
            NormalizationError, match="Maximum recursion depth \\(2\\) exceeded"
        ) as exc_info:
            normalize_id_keys(data, _max_depth=2)

        assert isinstance(exc_info.value.__cause__, RecursionError)
        assert exc_info.value.data == "value"  # Stores data where limit hit

    def test_int_keys_dict_values_error_handling(self, mocker: "MockerFixture"):
        # Tests cast failure when normalize returns non-dict for dict value
        import evedata_platform_static._utils._normalize_id_keys as module  # noqa: PLC0415

        data = {1: {"nested": "value"}}
        original_normalize = module.normalize_id_keys

        def mock_normalize(d: Any, **kwargs: Any) -> Any:
            if d == {"nested": "value"}:
                return "not_a_dict"
            return original_normalize(d, **kwargs)

        mocker.patch.object(module, "normalize_id_keys", side_effect=mock_normalize)

        with pytest.raises(
            module.NormalizationError, match="Failed to normalize dict values"
        ):
            module.normalize_id_keys(data)

    def test_string_keys_dict_values_error_handling(self, mocker: "MockerFixture"):
        import evedata_platform_static._utils._normalize_id_keys as module  # noqa: PLC0415

        data = {"key1": {"nested": "value"}}
        original_normalize = module.normalize_id_keys
        call_count = 0

        def mock_normalize(d: Any, **kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return original_normalize(d, **kwargs)  # Let main call through
            msg = "Mocked error during recursion"
            raise TypeError(msg)

        mocker.patch.object(module, "normalize_id_keys", side_effect=mock_normalize)

        with pytest.raises(
            module.NormalizationError,
            match="Failed to normalize dict values.*Mocked error",
        ):
            module.normalize_id_keys(data)
