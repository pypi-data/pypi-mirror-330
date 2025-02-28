# Synchronous Operations

This guide covers how to use the synchronous API for database operations with the Manticore CockroachDB client.

## Connecting to the Database

You can connect to a CockroachDB database using the `Database` class:

```python
from manticore_cockroachdb import Database

# Connect with individual parameters
db = Database(
    host="localhost",
    port=26257,
    database="example_db",
    user="root",
    password="",
    ssl_mode="disable"
)

# Or connect using a connection URL
db = Database.from_url("postgresql://root@localhost:26257/example_db?sslmode=disable")
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
db.create_table("users", users_schema, if_not_exists=True)
```

### Inserting Data

```python
# Insert a single record
user_id = db.insert("users", {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
})

# Insert multiple records
db.batch_insert("users", [
    {"name": "Alice Smith", "email": "alice@example.com", "age": 25},
    {"name": "Bob Johnson", "email": "bob@example.com", "age": 35}
])
```

### Querying Data

```python
# Select all records
all_users = db.select("users")

# Select with conditions
active_users = db.select("users", where={"active": True})

# Select with custom WHERE clause
young_users = db.select("users", where_clause="age < %s", params=[30])

# Select a single record
user = db.select_one("users", where={"id": user_id})

# Count records
user_count = db.count("users")
active_count = db.count("users", where={"active": True})
```

### Updating Data

```python
# Update a record
db.update("users", {"age": 31}, where={"id": user_id})

# Update with custom WHERE clause
db.update("users", {"active": False}, where_clause="age > %s", params=[40])
```

### Deleting Data

```python
# Delete a record
db.delete("users", where={"id": user_id})

# Delete with custom WHERE clause
db.delete("users", where_clause="created_at < %s", params=["2020-01-01"])
```

## Using Transactions

```python
# Start a transaction
with db.transaction():
    # All operations within this block are part of the same transaction
    db.insert("users", {"name": "Transaction User", "email": "tx@example.com"})
    db.update("users", {"active": False}, where={"email": "john@example.com"})
    
    # If any operation fails, the entire transaction is rolled back
    # If all operations succeed, the transaction is committed
```

## Using the Table Class

The `Table` class provides a more object-oriented approach to working with tables:

```python
from manticore_cockroachdb import Table

# Create a Table instance
users = Table("users", db=db)

# Create a record
user = users.create({
    "name": "Table User",
    "email": "table@example.com",
    "age": 28
})

# Read a record
retrieved_user = users.read(user["id"])

# Update a record
updated_user = users.update(user["id"], {"age": 29})

# Delete a record
users.delete(user["id"])

# List records
all_users = users.list()
active_users = users.list(where={"active": True})

# Count records
count = users.count()
```

## Batch Operations with Table

```python
# Batch create
batch_users = [
    {"name": "Batch User 1", "email": "batch1@example.com", "age": 21},
    {"name": "Batch User 2", "email": "batch2@example.com", "age": 22},
    {"name": "Batch User 3", "email": "batch3@example.com", "age": 23}
]
created_users = users.batch_create(batch_users)

# Batch update
updates = [
    {"id": created_users[0]["id"], "age": 31},
    {"id": created_users[1]["id"], "age": 32},
    {"id": created_users[2]["id"], "age": 33}
]
updated_users = users.batch_update(updates)

# Batch delete
ids_to_delete = [user["id"] for user in created_users]
users.batch_delete(ids_to_delete)
```

## Closing the Connection

Always close the database connection when you're done:

```python
db.close()
```

## Complete Example

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
    
    # Insert data
    user = users.create({
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    })
    print(f"Created user: {user['name']} with ID: {user['id']}")
    
    # Update data
    updated_user = users.update(user["id"], {"age": 31})
    print(f"Updated user age: {updated_user['age']}")
    
    # Query data
    all_users = users.list()
    print(f"Total users: {len(all_users)}")
    
    # Delete data
    users.delete(user["id"])
    print("User deleted")
    
finally:
    # Close connection
    db.close()
``` 