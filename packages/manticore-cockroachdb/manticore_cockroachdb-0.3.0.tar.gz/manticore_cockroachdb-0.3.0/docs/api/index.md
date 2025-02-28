# API Reference

The Manticore CockroachDB client provides a comprehensive API for interacting with CockroachDB databases. This section documents all the classes and methods available in the library.

## Core Components

- [Database](database.md): Synchronous database connection and operations
- [AsyncDatabase](async_database.md): Asynchronous database connection and operations
- [Migrations](migrations.md): Database schema migration tools (both sync and async)
- [Table](table.md): Synchronous CRUD operations on database tables
- [AsyncTable](async_table.md): Asynchronous CRUD operations on database tables
- [Exceptions](exceptions.md): Custom exceptions defined by the library

## Module Structure

```
manticore_cockroachdb/
├── __init__.py             # Package exports
├── database.py             # Synchronous Database implementation
├── async_database.py       # Asynchronous Database implementation
├── migration.py            # Synchronous Migration implementation
├── async_migration.py      # Asynchronous Migration implementation
├── crud/
│   ├── __init__.py         # CRUD package exports
│   ├── table.py            # Synchronous Table implementation
│   ├── async_table.py      # Asynchronous Table implementation
│   └── exceptions.py       # Custom exceptions
```

## Import Conventions

For convenience, the main classes are exported at the package level:

```python
# Synchronous API
from manticore_cockroachdb import Database, Table, Migration

# Asynchronous API
from manticore_cockroachdb import AsyncDatabase, AsyncTable, AsyncMigration

# Exceptions
from manticore_cockroachdb.crud.exceptions import TableNotInitializedError
```

## Using the API Documentation

Each page in this section includes:

1. Class definitions with inheritance information
2. Constructor parameters and their descriptions
3. Method signatures with parameter descriptions and return types
4. Code examples demonstrating common usage patterns
5. Important notes and warnings about edge cases or potential issues

## Type Annotations

The library uses Python type annotations throughout to provide better IDE integration and improve code quality. The API documentation includes these type annotations to make it clear what types are expected and returned.

## Thread Safety

- The synchronous API (`Database`, `Table`, etc.) is thread-safe for read operations but requires external synchronization for write operations.
- The asynchronous API (`AsyncDatabase`, `AsyncTable`, etc.) is designed for concurrent use within the asyncio framework.

## Connection Pooling

Both the synchronous and asynchronous APIs use connection pooling for efficient database access. This is handled automatically, but you can configure pool settings when creating a database instance. 