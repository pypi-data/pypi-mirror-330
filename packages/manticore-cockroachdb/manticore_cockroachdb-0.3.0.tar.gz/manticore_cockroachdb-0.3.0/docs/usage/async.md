# Asynchronous Operations

This guide covers how to use the asynchronous API for database operations with the Manticore CockroachDB client.

## Connecting to the Database

You can connect to a CockroachDB database using the `AsyncDatabase` class:

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase

async def main():
    # Connect with individual parameters
    db = AsyncDatabase(
        host="localhost",
        port=26257,
        database="example_db",
        user="root",
        password="",
        ssl_mode="disable"
    )
    
    # Or connect using a connection URL
    # db = AsyncDatabase.from_url("postgresql://root@localhost:26257/example_db?sslmode=disable")
    
    # Connect to the database
    await db.connect()
    
    try:
        # Perform database operations here
        pass
    finally:
        # Close the connection
        await db.close()

# Run the async function
asyncio.run(main())
```

## Basic Operations

### Creating Tables

```python
# Define table schema
users_schema = {
    "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
    "name": "TEXT NOT NULL",
    "email": "TEXT UNIQUE NOT NULL",
    "age": "INTEGER",
    "active": "BOOLEAN DEFAULT TRUE",
    "created_at": "TIMESTAMPTZ DEFAULT now()"
}

# Create the table
await db.create_table("async_users", users_schema, if_not_exists=True)
```

### Inserting Data

```python
# Insert a single record
user_id = await db.insert("async_users", {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
})

# Insert multiple records
await db.batch_insert("async_users", [
    {"name": "Alice Smith", "email": "alice@example.com", "age": 25},
    {"name": "Bob Johnson", "email": "bob@example.com", "age": 35}
])
```

### Querying Data

```python
# Select all records
all_users = await db.select("async_users")

# Select with conditions
active_users = await db.select("async_users", where={"active": True})

# Select with custom WHERE clause
young_users = await db.select("async_users", where_clause="age < %s", params=[30])

# Select a single record
user = await db.select_one("async_users", where={"id": user_id})

# Count records
user_count = await db.count("async_users")
active_count = await db.count("async_users", where={"active": True})
```

### Updating Data

```python
# Update a record
await db.update("async_users", {"age": 31}, where={"id": user_id})

# Update with custom WHERE clause
await db.update("async_users", {"active": False}, where_clause="age > %s", params=[40])
```

### Deleting Data

```python
# Delete a record
await db.delete("async_users", where={"id": user_id})

# Delete with custom WHERE clause
await db.delete("async_users", where_clause="created_at < %s", params=["2020-01-01"])
```

## Using Transactions

```python
# Start a transaction
async with db.transaction():
    # All operations within this block are part of the same transaction
    await db.insert("async_users", {"name": "Transaction User", "email": "tx@example.com"})
    await db.update("async_users", {"active": False}, where={"email": "john@example.com"})
    
    # If any operation fails, the entire transaction is rolled back
    # If all operations succeed, the transaction is committed
```

## Using the AsyncTable Class

The `AsyncTable` class provides a more object-oriented approach to working with tables:

```python
from manticore_cockroachdb import AsyncTable

# Create an AsyncTable instance
users = AsyncTable("async_users", db=db)
await users.initialize()

# Create a record
user = await users.create({
    "name": "Table User",
    "email": "table@example.com",
    "age": 28
})

# Read a record
retrieved_user = await users.read(user["id"])

# Update a record
updated_user = await users.update(user["id"], {"age": 29})

# Delete a record
await users.delete(user["id"])

# List records
all_users = await users.list()
active_users = await users.list(where={"active": True})

# Count records
count = await users.count()
```

## Batch Operations with AsyncTable

```python
# Batch create
batch_users = [
    {"name": "Batch User 1", "email": "batch1@example.com", "age": 21},
    {"name": "Batch User 2", "email": "batch2@example.com", "age": 22},
    {"name": "Batch User 3", "email": "batch3@example.com", "age": 23}
]
created_users = await users.batch_create(batch_users)

# Batch update
updates = [
    {"id": created_users[0]["id"], "age": 31},
    {"id": created_users[1]["id"], "age": 32},
    {"id": created_users[2]["id"], "age": 33}
]
updated_users = await users.batch_update(updates)

# Batch delete
ids_to_delete = [user["id"] for user in created_users]
await users.batch_delete(ids_to_delete)
```

## Complete Example

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase, AsyncTable

async def main():
    # Connect to database
    db = AsyncDatabase(database="example_db")
    await db.connect()
    
    try:
        # Create table
        await db.create_table(
            "async_users",
            {
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "name": "TEXT NOT NULL",
                "email": "TEXT UNIQUE NOT NULL",
                "age": "INTEGER",
                "active": "BOOLEAN DEFAULT TRUE"
            },
            if_not_exists=True
        )
        
        # Create AsyncTable instance
        users = AsyncTable("async_users", db=db)
        await users.initialize()
        
        # Insert data
        user = await users.create({
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        })
        print(f"Created user: {user['name']} with ID: {user['id']}")
        
        # Update data
        updated_user = await users.update(user["id"], {"age": 31})
        print(f"Updated user age: {updated_user['age']}")
        
        # Query data
        all_users = await users.list()
        print(f"Total users: {len(all_users)}")
        
        # Delete data
        await users.delete(user["id"])
        print("User deleted")
        
    finally:
        # Close connection
        await db.close()

# Run the async function
asyncio.run(main())
``` 