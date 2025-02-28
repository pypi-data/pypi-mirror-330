# Manticore CockroachDB Client

A Python client for [CockroachDB](https://www.cockroachlabs.com/) with synchronous and asynchronous support, simple CRUD operations, schema migrations, and extensive type annotations.

## Features

- **Dual Sync/Async API**: Choose between synchronous or asynchronous operations based on your needs.
- **Connection Pooling**: Efficient connection management for optimized database access.
- **Schema Migrations**: Built-in versioned schema migration system.
- **CRUD Table Operations**: Simplified Create, Read, Update, Delete operations.
- **Type Safety**: Comprehensive type annotations for better IDE support.
- **Security**: SSL/TLS connection support with certificate validation.

## Installation

Install from PyPI:

```bash
pip install manticore-cockroachdb
```

## Quick Start

### Synchronous Usage

```python
from manticore_cockroachdb import Database, Table

# Create a database connection
db = Database(database="mydb", host="localhost")

# Define a table
users = Table(
    "users",
    db=db,
    schema={
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "name": "TEXT NOT NULL",
        "email": "TEXT UNIQUE NOT NULL",
    }
)

# Initialize the table schema
users.initialize()

# Create a user
user = users.create({
    "name": "John Doe",
    "email": "john@example.com"
})

# Read the user
user = users.read(user["id"])
print(user)
```

### Asynchronous Usage

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase, AsyncTable

async def main():
    # Create a database connection
    db = AsyncDatabase(database="mydb", host="localhost")
    await db.connect()
    
    # Define a table
    users = AsyncTable(
        "users",
        db=db,
        schema={
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL",
        }
    )
    
    # Initialize the table schema
    await users.initialize()
    
    # Create a user
    user = await users.create({
        "name": "John Doe",
        "email": "john@example.com"
    })
    
    # Read the user
    user = await users.read(user["id"])
    print(user)
    
    await db.close()

# Run the async function
asyncio.run(main())
```

## License

MIT License

## Credits

Developed by [Manticore Technology](https://github.com/manticoretechnology). 