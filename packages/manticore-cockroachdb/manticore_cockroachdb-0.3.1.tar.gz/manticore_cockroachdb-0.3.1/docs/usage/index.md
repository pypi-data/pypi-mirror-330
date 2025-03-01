# Usage Guide

Welcome to the Manticore CockroachDB client usage guide. This section provides comprehensive documentation on how to use the library for various database operations.

## Overview

The Manticore CockroachDB client provides both synchronous and asynchronous APIs for interacting with CockroachDB databases. The library is designed to be simple to use while providing powerful features for database operations.

## Sections

- [Synchronous Operations](sync.md): Learn how to use the synchronous API for database operations.
- [Asynchronous Operations](async.md): Learn how to use the asynchronous API for database operations.
- [Migrations](migrations.md): Learn how to manage database schema changes using migrations.
- [CRUD Operations](crud.md): Learn how to perform Create, Read, Update, and Delete operations.
- [Advanced Usage](advanced.md): Learn about advanced usage patterns and techniques.

## Quick Start

Here's a quick example to get you started with the synchronous API:

```python
from manticore_cockroachdb import Database, Table

# Connect to database
db = Database(database="example_db")

try:
    # Create a table
    db.create_table(
        "users",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL",
            "age": "INTEGER"
        },
        if_not_exists=True
    )
    
    # Create a Table instance
    users = Table("users", db=db)
    
    # Create a user
    user = users.create({
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    })
    print(f"Created user with ID: {user['id']}")
    
    # Read the user
    retrieved_user = users.read(user["id"])
    print(f"Retrieved user: {retrieved_user['name']}")
    
    # Update the user
    updated_user = users.update(user["id"], {"age": 31})
    print(f"Updated user age: {updated_user['age']}")
    
    # Delete the user
    users.delete(user["id"])
    print("User deleted")
    
finally:
    # Close the database connection
    db.close()
```

And here's a quick example using the asynchronous API:

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase, AsyncTable

async def main():
    # Connect to database
    db = AsyncDatabase(database="example_db")
    await db.connect()
    
    try:
        # Create a table
        await db.create_table(
            "async_users",
            {
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "name": "TEXT NOT NULL",
                "email": "TEXT UNIQUE NOT NULL",
                "age": "INTEGER"
            },
            if_not_exists=True
        )
        
        # Create an AsyncTable instance
        users = AsyncTable("async_users", db=db)
        await users.initialize()
        
        # Create a user
        user = await users.create({
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        })
        print(f"Created user with ID: {user['id']}")
        
        # Read the user
        retrieved_user = await users.read(user["id"])
        print(f"Retrieved user: {retrieved_user['name']}")
        
        # Update the user
        updated_user = await users.update(user["id"], {"age": 31})
        print(f"Updated user age: {updated_user['age']}")
        
        # Delete the user
        await users.delete(user["id"])
        print("User deleted")
        
    finally:
        # Close the database connection
        await db.close()

# Run the async function
asyncio.run(main())
```

## Available Topics

- [Sync Operations](sync.md): Learn how to use the synchronous API for basic and advanced database operations.
- [Async Operations](async.md): Discover how to leverage the asynchronous API for non-blocking database operations.
- [Migrations](migrations.md): Understand how to manage database schema changes over time.
- [CRUD Operations](crud.md): Explore the simplified Create, Read, Update, Delete operations.
- [Advanced Usage](advanced.md): Dive into advanced features like transactions, connection pooling, and more.

## Choosing Between Sync and Async APIs

The Manticore CockroachDB client offers two distinct APIs:

### Synchronous API
Use the synchronous API when:
- You're building a simple script or application
- You need straightforward, sequential code
- Your application doesn't have demanding concurrency requirements
- You're working in a traditional synchronous web framework

### Asynchronous API
Use the asynchronous API when:
- You're building a high-performance application that needs to handle many concurrent operations
- You're already using an asynchronous framework like FastAPI, Starlette, or aiohttp
- You need non-blocking I/O operations for better scalability
- You want to leverage Python's asyncio capabilities

Both APIs offer the same set of features, so your choice depends primarily on your application's architecture and performance requirements.

## Common Usage Patterns

Regardless of whether you choose the synchronous or asynchronous API, the library follows consistent patterns for database operations:

1. **Connection Management**: Create and manage database connections
2. **Table Operations**: Define, create, and modify tables
3. **CRUD Operations**: Perform Create, Read, Update, Delete operations on table records
4. **Transactions**: Manage database transactions for atomic operations
5. **Migrations**: Handle database schema changes over time

Each topic in this section explores these patterns in detail, providing examples and best practices. 