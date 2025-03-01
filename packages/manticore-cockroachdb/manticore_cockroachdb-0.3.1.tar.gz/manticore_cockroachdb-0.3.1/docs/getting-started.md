# Getting Started

This guide will help you get started with the Manticore CockroachDB client library. We'll cover installation, basic setup, and simple examples of both synchronous and asynchronous usage.

## Prerequisites

Before using this library, you need:

- Python 3.8 or higher
- A running CockroachDB instance (local or remote)

## Installation

You can install the Manticore CockroachDB client using pip:

```bash
pip install manticore-cockroachdb
```

For development, you might want to install additional dependencies:

```bash
pip install manticore-cockroachdb[dev]  # Includes testing and development tools
pip install manticore-cockroachdb[docs]  # Includes documentation tools
```

## Setting Up a Database Connection

The first step is to create a database connection. You can use either synchronous or asynchronous connections depending on your needs.

### Synchronous Connection

```python
from manticore_cockroachdb import Database

# Connect to a local CockroachDB instance
db = Database(
    database="mydatabase",  # Database name
    host="localhost",       # Database host
    port=26257,             # CockroachDB port (default: 26257)
    user="root",            # Database user
    password=None,          # Database password
    sslmode="disable"       # SSL mode (options: disable, require, verify-ca, verify-full)
)

# For production, you'll want to enable SSL:
db_secure = Database(
    database="mydatabase",
    host="your-cockroach-cluster.example.com",
    user="dbuser",
    password="your-password",
    sslmode="verify-full"
)
```

### Asynchronous Connection

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase

async def setup_db():
    # Connect to a local CockroachDB instance
    db = AsyncDatabase(
        database="mydatabase",  # Database name
        host="localhost",       # Database host
        port=26257,             # CockroachDB port (default: 26257)
        user="root",            # Database user
        password=None,          # Database password
        sslmode="disable"       # SSL mode (options: disable, require, verify-ca, verify-full)
    )
    
    await db.connect()  # Establish connection
    return db

# Example usage
async def main():
    db = await setup_db()
    # Use the database...
    await db.close()  # Close connection when done

asyncio.run(main())
```

## Creating Tables

The library provides a simple way to define and create database tables.

### Synchronous Table Creation

```python
from manticore_cockroachdb import Database, Table

db = Database(database="mydatabase", host="localhost")

# Define a users table
users = Table(
    "users",                # Table name
    db=db,                  # Database connection
    schema={                # Schema definition
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "name": "TEXT NOT NULL",
        "email": "TEXT UNIQUE NOT NULL",
        "created_at": "TIMESTAMP DEFAULT NOW()",
    }
)

# Create the table
users.initialize()
```

### Asynchronous Table Creation

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase, AsyncTable

async def create_tables():
    db = AsyncDatabase(database="mydatabase", host="localhost")
    await db.connect()
    
    # Define a users table
    users = AsyncTable(
        "users",                # Table name
        db=db,                  # Database connection
        schema={                # Schema definition
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL",
            "created_at": "TIMESTAMP DEFAULT NOW()",
        }
    )
    
    # Create the table
    await users.initialize()
    
    return db, users

# Example usage
async def main():
    db, users_table = await create_tables()
    # Use the tables...
    await db.close()

asyncio.run(main())
```

## Next Steps

Now that you have set up a basic connection and created a table, you're ready to:

1. Perform CRUD operations (see [CRUD Operations](usage/crud.md))
2. Set up schema migrations (see [Migrations](usage/migrations.md))
3. Use advanced database features (see [Advanced Usage](usage/advanced.md))

For more examples, check out the [Examples](examples/index.md) section. 