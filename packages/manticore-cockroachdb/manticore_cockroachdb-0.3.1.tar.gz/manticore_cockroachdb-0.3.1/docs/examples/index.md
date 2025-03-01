# Examples

This section provides practical examples of using the Manticore CockroachDB client in various scenarios. These examples are designed to help you understand how to use the library effectively for your own projects.

## Available Examples

- [Sync Examples](sync_examples.md): Examples using the synchronous API
- [Async Examples](async_examples.md): Examples using the asynchronous API
- [Migration Examples](migration_examples.md): Examples of database schema migrations

## Basic Example

Here's a simple example to get you started with the library:

```python
from manticore_cockroachdb import Database, Table

# Connect to database
db = Database(
    database="mydb",
    host="localhost",
    port=26257,
    user="root",
    sslmode="disable"
)

# Define and create a users table
users = Table(
    "users",
    db=db,
    schema={
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "username": "TEXT NOT NULL UNIQUE",
        "email": "TEXT NOT NULL",
        "created_at": "TIMESTAMP NOT NULL DEFAULT NOW()"
    }
)
users.initialize()

# Create a user
new_user = users.create({
    "username": "johndoe",
    "email": "john@example.com"
})
print(f"Created user with ID: {new_user['id']}")

# Query users
all_users = users.list()
for user in all_users:
    print(f"User: {user['username']}, Email: {user['email']}")
```

## Async Example

Here's the same example using the asynchronous API:

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase, AsyncTable

async def main():
    # Connect to database
    db = AsyncDatabase(
        database="mydb",
        host="localhost",
        port=26257,
        user="root",
        sslmode="disable"
    )
    await db.connect()
    
    # Define and create a users table
    users = AsyncTable(
        "users",
        db=db,
        schema={
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "username": "TEXT NOT NULL UNIQUE",
            "email": "TEXT NOT NULL",
            "created_at": "TIMESTAMP NOT NULL DEFAULT NOW()"
        }
    )
    await users.initialize()
    
    # Create a user
    new_user = await users.create({
        "username": "johndoe",
        "email": "john@example.com"
    })
    print(f"Created user with ID: {new_user['id']}")
    
    # Query users
    all_users = await users.list()
    for user in all_users:
        print(f"User: {user['username']}, Email: {user['email']}")
    
    await db.close()

asyncio.run(main())
```

## Example Scenarios

The examples in this section cover a variety of real-world scenarios, including:

- Basic CRUD operations
- Complex queries with filtering and ordering
- Transaction management
- Connection pooling optimization
- Schema migrations and versioning
- Advanced database patterns

Each example includes complete code snippets that you can adapt for your own projects, along with explanations of key concepts and best practices. 