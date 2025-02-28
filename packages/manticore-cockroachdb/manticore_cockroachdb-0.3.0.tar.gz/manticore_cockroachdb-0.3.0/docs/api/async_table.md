# AsyncTable

::: manticore_cockroachdb.crud.async_table.AsyncTable

## Overview

The `AsyncTable` class provides a high-level, asynchronous interface for interacting with database tables. It encapsulates common CRUD (Create, Read, Update, Delete) operations and handles table initialization automatically.

## Basic Usage

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase, AsyncTable

async def main():
    # Create database connection
    db = AsyncDatabase(database="mydb", host="localhost")
    await db.connect()
    
    # Define a users table
    users = AsyncTable(
        "users",
        db=db,
        schema={
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL",
        }
    )
    
    # Initialize the table (creates it if it doesn't exist)
    await users.initialize()
    
    # Create a user
    user = await users.create({
        "name": "John Doe",
        "email": "john@example.com"
    })
    
    print(f"Created user: {user}")
    
    # Read the user
    retrieved_user = await users.read(user["id"])
    print(f"Retrieved user: {retrieved_user}")
    
    # Update the user
    updated_user = await users.update(user["id"], {"name": "Jane Doe"})
    print(f"Updated user: {updated_user}")
    
    # List users
    all_users = await users.list()
    print(f"All users: {all_users}")
    
    # Count users
    count = await users.count()
    print(f"User count: {count}")
    
    # Delete the user
    deleted = await users.delete(user["id"])
    print(f"User deleted: {deleted}")
    
    await db.close()

asyncio.run(main())
```

## CRUD Operations

### Creating Records

The `create` method inserts a new record into the table:

```python
user = await users_table.create({
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
})

# user contains the full record, including any default values and generated IDs
print(user["id"])  # The generated UUID
```

### Reading Records

The `read` method retrieves a record by its ID:

```python
user = await users_table.read("550e8400-e29b-41d4-a716-446655440000")
if user:
    print(f"Found user: {user['name']}")
else:
    print("User not found")
```

### Updating Records

The `update` method modifies an existing record:

```python
updated_user = await users_table.update(
    "550e8400-e29b-41d4-a716-446655440000",
    {
        "name": "John Smith",
        "age": 31
    }
)

if updated_user:
    print(f"Updated user: {updated_user}")
else:
    print("User not found")
```

### Deleting Records

The `delete` method removes a record from the table:

```python
success = await users_table.delete("550e8400-e29b-41d4-a716-446655440000")
if success:
    print("User deleted successfully")
else:
    print("User not found or could not be deleted")
```

## Batch Operations

### Batch Creation

The `batch_create` method inserts multiple records in a single transaction:

```python
users = [
    {"name": "User 1", "email": "user1@example.com"},
    {"name": "User 2", "email": "user2@example.com"},
    {"name": "User 3", "email": "user3@example.com"},
]

created_users = await users_table.batch_create(users)
print(f"Created {len(created_users)} users")
```

### Batch Updates

The `batch_update` method updates multiple records in a single transaction:

```python
updates = [
    {"id": "id1", "active": False},
    {"id": "id2", "active": False},
    {"id": "id3", "active": True},
]

updated_users = await users_table.batch_update(updates)
print(f"Updated {len(updated_users)} users")
```

## Query Operations

### Listing Records

The `list` method retrieves multiple records with filtering, ordering, and limits:

```python
# Get all users
all_users = await users_table.list()

# Get users with filtering
active_users = await users_table.list(where={"active": True})

# Get users with ordering
sorted_users = await users_table.list(order_by="name ASC")

# Get users with limit
first_10_users = await users_table.list(limit=10)

# Combine options
result = await users_table.list(
    where={"active": True},
    order_by="created_at DESC",
    limit=5
)
```

### Counting Records

The `count` method counts records, optionally with filters:

```python
# Count all users
total_users = await users_table.count()

# Count with filters
active_count = await users_table.count(where={"active": True})
```

## Using as a Context Manager

```python
async with AsyncTable("users", db=db) as users:
    # Table is automatically initialized
    user = await users.create({"name": "John", "email": "john@example.com"})
    # ... perform more operations
    # No need to call initialize() or worry about cleanup
``` 