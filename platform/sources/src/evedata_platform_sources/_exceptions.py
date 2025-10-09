class SourceError(Exception):
    """Base class for all platform source errors."""


class HDESourceError(SourceError):
    """Base class for HDE source errors."""


class HDENotArchivedError(HDESourceError):
    """Raised when there is no HDE archive."""


class HDEArchiveExistsError(HDESourceError):
    """Raised when an HDE archive already exists."""

    def __init__(self, version: int):
        """Initialize a new HDEArchiveExistsError."""
        self.version = version
        super().__init__(f"HDE archive already exists: {version}")


class HDEArchiveNotFoundError(HDESourceError):
    """Raised when an HDE archive was not found."""

    def __init__(self, version: int):
        """Initialize a new HDEArchiveNotFoundError."""
        self.version = version
        super().__init__(f"HDE archive not found: {version}")


class SDESourceError(SourceError):
    """Base class for SDE source errors."""


class SDENotArchivedError(SDESourceError):
    """Raised when there is no SDE archive."""


class SDEArchiveExistsError(SDESourceError):
    """Raised when an SDE archive already exists."""

    def __init__(self, version: int):
        """Initialize a new SDEArchiveExistsError."""
        self.version = version
        super().__init__(f"SDE archive already exists: {version}")


class SDEArchiveNotFoundError(SDESourceError):
    """Raised when an SDE archive was not found."""

    def __init__(self, version: int):
        """Initialize a new SDEArchiveNotFoundError."""
        self.version = version
        super().__init__(f"SDE archive not found: {version}")
