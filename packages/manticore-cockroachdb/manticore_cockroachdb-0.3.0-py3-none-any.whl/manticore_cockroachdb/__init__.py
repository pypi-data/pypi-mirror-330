"""CockroachDB database wrapper.

This package provides a high-level interface for managing CockroachDB databases.
"""

from .crud import DatabaseError, Table, ValidationError
from .crud.async_table import AsyncTable
from .database import Database, Transaction
from .async_database import AsyncDatabase, AsyncTransaction
from .migration import Migration, Migrator
from .async_migration import AsyncMigration, AsyncMigrator

__version__ = "0.3.0"
__all__ = [
    # Synchronous components
    "Database",
    "Transaction",
    "Migration",
    "Migrator",
    "Table",
    
    # Asynchronous components
    "AsyncDatabase",
    "AsyncTransaction",
    "AsyncMigration",
    "AsyncMigrator",
    "AsyncTable",
    
    # Exceptions
    "DatabaseError",
    "ValidationError",
] 