"""Exceptions for CRUD operations."""


class DatabaseError(Exception):
    """Base class for database errors."""
    pass


class ValidationError(Exception):
    """Raised when record data is invalid."""
    pass


class TableNotInitializedError(Exception):
    """Raised when trying to use a table that has not been initialized."""
    pass 