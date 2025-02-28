# Manticore CockroachDB

A robust Python client library for CockroachDB that provides both synchronous and asynchronous interfaces, with features like connection pooling, transaction management, migrations, and high-level CRUD abstractions.

## Features

- **Dual interfaces**: Synchronous and asynchronous APIs for flexible integration
- **Connection pooling**: Efficient database connection management
- **Transaction management**: Simplified transaction handling with automatic retries
- **Database migrations**: Forward and rollback migrations for schema management
- **High-level abstractions**: Table classes for simplified CRUD operations
- **Developer-friendly**: Intuitive APIs designed for developer productivity
- **CockroachDB optimized**: Built with CockroachDB's distributed nature in mind

## Installation

```bash
pip install manticore-cockroachdb
```

## Quick Start

### Synchronous Usage

```python
from manticore_cockroachdb.database import Database
from manticore_cockroachdb.crud.table import Table

# Connect to database
db = Database(database="my_database")

# Create a table
users_schema = {
    "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
    "name": "TEXT NOT NULL",
    "email": "TEXT UNIQUE NOT NULL"
}
db.create_table("users", users_schema)

# Create a Table instance for easier CRUD operations
users = Table("users", db=db)

# Create a user
user = users.create({
    "name": "John Doe",
    "email": "john@example.com"
})

# Read the user
retrieved_user = users.read(user["id"])

# Update the user
updated_user = users.update(user["id"], {"name": "Jane Doe"})

# Delete the user
deleted = users.delete(user["id"])

# Close the database connection
db.close()
```

### Asynchronous Usage

```python
import asyncio
from manticore_cockroachdb.async_database import AsyncDatabase
from manticore_cockroachdb.crud.async_table import AsyncTable

async def main():
    # Connect to database
    db = AsyncDatabase(database="my_database")
    await db.connect()
    
    try:
        # Create a table
        users_schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL"
        }
        await db.create_table("async_users", users_schema)
        
        # Create a Table instance
        users = AsyncTable("async_users", db=db)
        await users.initialize()
        
        # Create a user
        user = await users.create({
            "name": "John Doe",
            "email": "john@example.com"
        })
        
        # Read the user
        retrieved_user = await users.read(user["id"])
        
        # Update the user
        updated_user = await users.update(user["id"], {"name": "Jane Doe"})
        
        # Delete the user
        deleted = await users.delete(user["id"])
    
    finally:
        # Close the database connection
        await db.close()

# Run the async example
asyncio.run(main())
```

## Database Migrations

### Synchronous Migrations

```python
from manticore_cockroachdb.database import Database
from manticore_cockroachdb.migration import Migration

# Connect to database
db = Database(database="my_database")

# Create migration instance
migration = Migration(db, migrations_dir="./migrations")

# Create a migration
migration.create_migration(
    "create users table",
    """
    CREATE TABLE users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """,
    "DROP TABLE users;"
)

# Apply migrations
applied = migration.migrate()
print(f"Applied {applied} migrations")

# Rollback a migration
rollback_count = migration.rollback(count=1)
print(f"Rolled back {rollback_count} migrations")
```

### Asynchronous Migrations

```python
import asyncio
from manticore_cockroachdb.async_database import AsyncDatabase
from manticore_cockroachdb.async_migration import AsyncMigration

async def main():
    # Connect to database
    db = AsyncDatabase(database="my_database")
    await db.connect()
    
    try:
        # Create migration instance
        migration = AsyncMigration(db, migrations_dir="./migrations")
        
        # Create a migration
        await migration.create_migration(
            "create async users table",
            """
            CREATE TABLE async_users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            );
            """,
            "DROP TABLE async_users;"
        )
        
        # Apply migrations
        applied = await migration.migrate()
        print(f"Applied {applied} migrations")
        
        # Rollback a migration
        rollback_count = await migration.rollback(count=1)
        print(f"Rolled back {rollback_count} migrations")
    
    finally:
        await db.close()

# Run the async example
asyncio.run(main())
```

## Advanced Usage

### Transactions

```python
from manticore_cockroachdb.database import Database

# Connect to database
db = Database(database="my_database")

# Define transaction operation
def transfer_money(conn):
    with conn.cursor() as cur:
        # Deduct from one account
        cur.execute(
            "UPDATE accounts SET balance = balance - 100 WHERE id = %s",
            ("account1",)
        )
        
        # Add to another account
        cur.execute(
            "UPDATE accounts SET balance = balance + 100 WHERE id = %s",
            ("account2",)
        )
        
        # Get updated balances
        cur.execute(
            "SELECT * FROM accounts WHERE id IN (%s, %s)",
            ("account1", "account2")
        )
        return cur.fetchall()

# Run the transaction with automatic retries
result = db.run_in_transaction(transfer_money)
```

### Batch Operations

```python
from manticore_cockroachdb.crud.table import Table
from manticore_cockroachdb.database import Database

# Connect to database
db = Database(database="my_database")
users = Table("users", db=db)

# Batch create
users_to_create = [
    {"name": "User 1", "email": "user1@example.com"},
    {"name": "User 2", "email": "user2@example.com"},
    {"name": "User 3", "email": "user3@example.com"},
]
created_users = users.batch_create(users_to_create)

# Batch update
for user in created_users:
    user["name"] = user["name"] + " (Updated)"
updated_users = users.batch_update(created_users)
```

## Environment Variables

- `DATABASE_URL`: Database connection URL in format `postgresql://user:password@host:port/dbname?sslmode=mode`

## Examples

Check out the examples directory for complete working examples:

- `examples/basic_usage.py`: Basic synchronous usage
- `examples/async_usage.py`: Basic asynchronous usage
- `examples/migration_example.py`: Database migrations
- `examples/async_migration_example.py`: Asynchronous database migrations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 