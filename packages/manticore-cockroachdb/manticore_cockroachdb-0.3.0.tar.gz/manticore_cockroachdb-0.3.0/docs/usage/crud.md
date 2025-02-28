# CRUD Operations

This guide covers how to perform Create, Read, Update, and Delete (CRUD) operations using the Manticore CockroachDB client.

## Table Classes

The Manticore CockroachDB client provides two table classes for performing CRUD operations:

- `Table`: For synchronous operations
- `AsyncTable`: For asynchronous operations

These classes provide a more object-oriented approach to working with database tables compared to using the database classes directly.

## Synchronous CRUD Operations

### Creating a Table Instance

```python
from manticore_cockroachdb import Database, Table

# Connect to database
db = Database(database="example_db")

# Create a Table instance
users = Table("users", db=db)
```

### Creating Records

```python
# Create a single record
user = users.create({
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "active": True
})
print(f"Created user with ID: {user['id']}")

# Create multiple records in a batch
batch_users = [
    {"name": "Alice Smith", "email": "alice@example.com", "age": 25},
    {"name": "Bob Johnson", "email": "bob@example.com", "age": 35}
]
created_users = users.batch_create(batch_users)
print(f"Created {len(created_users)} users in batch")
```

### Reading Records

```python
# Read a record by ID
user = users.read(user_id)
print(f"User: {user['name']}, Email: {user['email']}")

# List all records
all_users = users.list()
print(f"Total users: {len(all_users)}")

# List records with conditions
active_users = users.list(where={"active": True})
print(f"Active users: {len(active_users)}")

# List records with custom WHERE clause
young_users = users.list(where_clause="age < %s", params=[30])
print(f"Young users: {len(young_users)}")

# Count records
count = users.count()
print(f"Total user count: {count}")

# Count records with conditions
active_count = users.count(where={"active": True})
print(f"Active user count: {active_count}")
```

### Updating Records

```python
# Update a record
updated_user = users.update(user_id, {"age": 31, "active": False})
print(f"Updated user: {updated_user['name']}, Age: {updated_user['age']}")

# Update multiple records in a batch
updates = [
    {"id": user_ids[0], "age": 26},
    {"id": user_ids[1], "age": 36}
]
updated_users = users.batch_update(updates)
print(f"Updated {len(updated_users)} users in batch")
```

### Deleting Records

```python
# Delete a record
users.delete(user_id)
print("User deleted")

# Delete multiple records in a batch
users.batch_delete(user_ids)
print(f"Deleted {len(user_ids)} users in batch")
```

## Asynchronous CRUD Operations

### Creating a Table Instance

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase, AsyncTable

async def main():
    # Connect to database
    db = AsyncDatabase(database="example_db")
    await db.connect()
    
    try:
        # Create an AsyncTable instance
        users = AsyncTable("async_users", db=db)
        await users.initialize()
        
        # Perform CRUD operations...
    finally:
        await db.close()

# Run the async function
asyncio.run(main())
```

### Creating Records

```python
# Create a single record
user = await users.create({
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "active": True
})
print(f"Created user with ID: {user['id']}")

# Create multiple records in a batch
batch_users = [
    {"name": "Alice Smith", "email": "alice@example.com", "age": 25},
    {"name": "Bob Johnson", "email": "bob@example.com", "age": 35}
]
created_users = await users.batch_create(batch_users)
print(f"Created {len(created_users)} users in batch")
```

### Reading Records

```python
# Read a record by ID
user = await users.read(user_id)
print(f"User: {user['name']}, Email: {user['email']}")

# List all records
all_users = await users.list()
print(f"Total users: {len(all_users)}")

# List records with conditions
active_users = await users.list(where={"active": True})
print(f"Active users: {len(active_users)}")

# List records with custom WHERE clause
young_users = await users.list(where_clause="age < %s", params=[30])
print(f"Young users: {len(young_users)}")

# Count records
count = await users.count()
print(f"Total user count: {count}")

# Count records with conditions
active_count = await users.count(where={"active": True})
print(f"Active user count: {active_count}")
```

### Updating Records

```python
# Update a record
updated_user = await users.update(user_id, {"age": 31, "active": False})
print(f"Updated user: {updated_user['name']}, Age: {updated_user['age']}")

# Update multiple records in a batch
updates = [
    {"id": user_ids[0], "age": 26},
    {"id": user_ids[1], "age": 36}
]
updated_users = await users.batch_update(updates)
print(f"Updated {len(updated_users)} users in batch")
```

### Deleting Records

```python
# Delete a record
await users.delete(user_id)
print("User deleted")

# Delete multiple records in a batch
await users.batch_delete(user_ids)
print(f"Deleted {len(user_ids)} users in batch")
```

## Error Handling

The table classes will raise appropriate exceptions if operations fail:

```python
from manticore_cockroachdb import Table
from manticore_cockroachdb.crud.exceptions import TableNotInitializedError

# Create a Table instance without initializing
users = Table("users")

try:
    # Attempt to use the table before initializing
    user = users.create({"name": "John Doe", "email": "john@example.com"})
except TableNotInitializedError as e:
    print(f"Error: {e}")
    # Initialize the table
    users.db = db
```

## Complete Example

### Synchronous Example

```python
from manticore_cockroachdb import Database, Table

# Connect to database
db = Database(database="example_db")

try:
    # Create table
    db.create_table(
        "users",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL",
            "age": "INTEGER",
            "active": "BOOLEAN DEFAULT TRUE"
        },
        if_not_exists=True
    )
    
    # Create Table instance
    users = Table("users", db=db)
    
    # Create records
    user1 = users.create({
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    })
    print(f"Created user: {user1['name']} with ID: {user1['id']}")
    
    user2 = users.create({
        "name": "Jane Smith",
        "email": "jane@example.com",
        "age": 28
    })
    print(f"Created user: {user2['name']} with ID: {user2['id']}")
    
    # Read records
    all_users = users.list()
    print(f"Total users: {len(all_users)}")
    
    # Update a record
    updated_user = users.update(user1["id"], {"age": 31})
    print(f"Updated user age: {updated_user['age']}")
    
    # Delete a record
    users.delete(user2["id"])
    print("User deleted")
    
    # Verify deletion
    remaining_users = users.list()
    print(f"Remaining users: {len(remaining_users)}")
    
finally:
    # Clean up
    db.drop_table("users", if_exists=True)
    
    # Close connection
    db.close()
```

### Asynchronous Example

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
        
        # Create records
        user1 = await users.create({
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        })
        print(f"Created user: {user1['name']} with ID: {user1['id']}")
        
        user2 = await users.create({
            "name": "Jane Smith",
            "email": "jane@example.com",
            "age": 28
        })
        print(f"Created user: {user2['name']} with ID: {user2['id']}")
        
        # Read records
        all_users = await users.list()
        print(f"Total users: {len(all_users)}")
        
        # Update a record
        updated_user = await users.update(user1["id"], {"age": 31})
        print(f"Updated user age: {updated_user['age']}")
        
        # Delete a record
        await users.delete(user2["id"])
        print("User deleted")
        
        # Verify deletion
        remaining_users = await users.list()
        print(f"Remaining users: {len(remaining_users)}")
        
    finally:
        # Clean up
        await db.drop_table("async_users", if_exists=True)
        
        # Close connection
        await db.close()

# Run the async function
asyncio.run(main())
``` 