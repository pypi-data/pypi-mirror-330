"""Exceptions for CRUD operations."""

from typing import Optional


class DatabaseError(Exception):
    """Base class for database errors."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        """Initialize database error.
        
        Args:
            message: Error message
            cause: Original exception that caused this error
        """
        super().__init__(message)
        self.__cause__ = cause


class ValidationError(Exception):
    """Raised when record data is invalid."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        """Initialize validation error.
        
        Args:
            message: Error message
            field: Field that failed validation
        """
        super().__init__(message)
        self.field = field


class TableNotInitializedError(DatabaseError):
    """Raised when trying to use a table that has not been initialized."""
    
    def __init__(self, table_name: str):
        """Initialize table not initialized error.
        
        Args:
            table_name: Name of the table that is not initialized
        """
        super().__init__(f"Table '{table_name}' is not initialized")
        self.table_name = table_name


class TableNotFoundError(DatabaseError):
    """Raised when trying to access a table that does not exist."""
    
    def __init__(self, table_name: str):
        """Initialize table not found error.
        
        Args:
            table_name: Name of the table that does not exist
        """
        super().__init__(f"Table '{table_name}' does not exist")
        self.table_name = table_name


class ConnectionError(DatabaseError):
    """Raised when a database connection cannot be established."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        """Initialize connection error.
        
        Args:
            message: Error message
            cause: Original exception that caused this error
        """
        super().__init__(f"Database connection error: {message}", cause)


class UniqueViolationError(DatabaseError):
    """Raised when a unique constraint is violated."""
    
    def __init__(self, constraint: str, message: Optional[str] = None):
        """Initialize unique violation error.
        
        Args:
            constraint: Name of the constraint that was violated
            message: Error message
        """
        msg = message or f"Unique constraint violation: {constraint}"
        super().__init__(msg)
        self.constraint = constraint 