# Instructions for working with Python code

## Tools

### Specific files

- `uv run pytest tests/path/to/test_file.py::TestClass::test_method`: Run a specific
  test
- `uv run ruff check path/to/file.py`: Run Python linters on a specific file
- `uv run ruff check --fix path/to/file.py`: Run Python linters and fix errors on a
  specific file
- `uv run ruff format path/to/file.py`: Format Python code in a specific file

## Workflow

- IMPORTANT: Never add imports to Python files as a standalone task. Unused imports will
  be removed by the linter.

## Coding style

- Python 3.11+ compatible code with runtime detection for 3.12+ optimizations

### Typing

- Always import `from __future__ import annotations`
- Import Python 3.11 features from `typing`, not `typing_extensions`
- Import only Python 3.12+ features or features with updates (e.g. `default` option for
  `TypeVar`) from `typing_extensions`
- Annotate all function parameters and return types
- Use specific types instead of `Any` where possible
- Use Union syntax (|) for simple unions, `typing.Union` for complex ones
- Use `Required`, `NotRequired`, and `ReadOnly` in `TypedDict`
- Apply `@override` to overridden methods
- Use `TypeIs` instead of `TypeGuard` for type narrowing
- Use `Self` instead of the class and for fluent interfaces and builder patterns
- Use function overloading when appropriate
- Use `LiteralString` for hardcoded values
- Use `Literal` for exact values
- Use `Final` for constants
- Use `NoReturn` for functions that never return
- Use `assert_never` for exhaustiveness checking
- Test type inference with `assert_type` and `reveal_type`
- NEVER use string literals for forward references
- ALWAYS specify variance for custom generic types when needed
- Use `ClassVar` for mutable class-level attributes and when type clarity is needed
- Use `Protocol` for structural subtyping instead of inheritance when appropriate
- Prefer `collections.abc` types over typing equivalents (e.g.,
  `collections.abc.Sequence` over `typing.List`)
- Use `TypeAlias` for simple type aliases (non-generic, no forward refs)
- Use `TypeAliasType` for generic type aliases or when you need lazy evaluation

### Class structure

IMPORTANT: Adhere to these templates when structuring classes.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, ClassVar, Protocol


class StandardClass:
    """1. Class docstring always comes first."""

    # 2. Class-level attributes and constants
    CLASS_CONSTANT: ClassVar[str] = "IMMUTABLE_VALUE"
    DEFAULT_CONFIG: ClassVar[dict[str, Any]] = {"timeout": 30}

    # Class variables with type annotations
    _registry: ClassVar[dict[str, type]] = {}
    instance_count: ClassVar[int] = 0

    # 3. Special methods (dunder methods) in lifecycle order
    def __new__(cls, *args: Any, **kwargs: Any) -> 'StandardClass':
        """Object creation (rarely needed)."""

    def __init__(self, param1: str, param2: int = 0) -> None:
        """Object initialization."""
        self._param1 = param1
        self._param2 = param2

    # String representation methods
    def __str__(self) -> str:
        """Human-readable string representation."""

    def __repr__(self) -> str:
        """Developer-friendly representation."""

    # Comparison methods
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""

    def __lt__(self, other: 'StandardClass') -> bool:
        """Less-than comparison (enables sorting)."""

    def __hash__(self) -> int:
        """Hash for use in sets/dicts."""

    # Container protocol methods
    def __len__(self) -> int:
        """Length/size of the object."""

    def __getitem__(self, key: Any) -> Any:
        """Item access via brackets."""

    def __contains__(self, item: Any) -> bool:
        """Membership testing with 'in'."""

    # Context manager protocol
    def __enter__(self) -> 'StandardClass':
        """Enter context (with statement)."""

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context (with statement)."""

    # 4. Properties (public interface)
    @property
    def param1(self) -> str:
        """Public property with getter."""
        return self._param1

    @param1.setter
    def param1(self, value: str) -> None:
        """Property setter."""
        self._param1 = value

    @property
    def computed_property(self) -> float:
        """Read-only computed property."""

    # 5. Class methods and static methods
    @classmethod
    def from_alternative(cls, data: dict[str, Any]) -> 'StandardClass':
        """Alternative constructor class method."""

    @classmethod
    def get_registry(cls) -> dict[str, type]:
        """Class method accessing class state."""
        return cls._registry

    @staticmethod
    def utility_function(value: Any) -> bool:
        """Static method (no class/instance access)."""

    # 6. Public instance methods (primary interface)
    def primary_action(self, arg: str) -> None:
        """Main public method."""

    def secondary_action(self, data: list[Any]) -> dict[str, Any]:
        """Another public method."""

    async def async_action(self) -> None:
        """Async public method."""

    # 7. Protected/internal methods (single underscore)
    def _internal_helper(self) -> None:
        """Protected method for subclasses."""

    def _validate_state(self) -> bool:
        """Internal validation method."""

    # 8. Private methods (double underscore, name mangled)
    def __private_implementation(self) -> None:
        """Truly private method."""


@dataclass
class DataclassExample:
    """1. Docstring first for dataclasses too."""

    # 2. Field declarations (replace __init__)
    required_field: str
    optional_field: int = 0
    mutable_field: list[str] = field(default_factory=list)

    # 3. __post_init__ for additional initialization
    def __post_init__(self) -> None:
        """Post-initialization processing."""

    # 4. Continue with standard ordering (properties, methods, etc.)
    @property
    def computed(self) -> str:
        """Properties after fields."""


class AbstractBase(ABC):
    """1. Abstract base class docstring."""

    # 2. Abstract properties come first
    @property
    @abstractmethod
    def required_property(self) -> str:
        """Subclasses must implement this property."""
        ...

    # 3. Abstract methods
    @abstractmethod
    def required_method(self, value: Any) -> None:
        """Subclasses must implement this method."""
        ...

    # 4. Concrete methods that use the abstract interface
    def template_method(self) -> None:
        """Concrete method using abstract parts."""


class ProtocolExample(Protocol):
    """1. Protocol docstring."""

    # 2. Protocol attributes (if any)
    attribute: int

    # 3. Protocol methods (no implementation)
    def required_method(self, x: float) -> str:
        """Method signature that implementations must match."""
        ...

    # 4. Concrete default methods (if any)
    def helper_method(self) -> None:
        """Default implementation provided by protocol."""
        ...
```

### Testing
