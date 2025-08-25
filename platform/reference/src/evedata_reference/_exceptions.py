from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class EVEDataException(Exception):  # noqa: N818
    """Base class for all SDE-related exceptions."""


class SDEDirectoryNotFound(EVEDataException):
    """Raised when the SDE directory is not found."""

    def __init__(self, path: "str | Path"):
        super().__init__(f"SDE directory not found: {path}")
        self.path = path


class SDEFilesNotFound(EVEDataException):
    """Raised when no SDE files are found in the specified directory."""

    def __init__(self, path: "str | Path"):
        super().__init__(f"No SDE files found in: {path}")
        self.path = path


class SDEFileNotFound(EVEDataException):
    """Raised when a specific SDE file is not found."""

    def __init__(self, path: "str | Path"):
        super().__init__(f"SDE file not found: {path}")
        self.path = path


class UnsupportedDestinationError(EVEDataException):
    """Raised when an unsupported destination format is specified."""

    def __init__(self, destination: str, supported: list[str] | None = None):
        if supported:
            message = (
                f"Unsupported destination: '{destination}'."
                f" Supported formats: {', '.join(supported)}"
            )
        else:
            message = f"Unsupported destination: '{destination}'"
        super().__init__(message)
        self.destination = destination
        self.supported = supported


class ESIError(EVEDataException):
    """Raised for general ESI-related errors."""


class ESIErrorLimitReachedError(ESIError):
    """Raised when the ESI error limit is reached."""
