# Advanced Usage

This guide covers advanced usage patterns and techniques for the Manticore CockroachDB client.

## Connection Pooling

Both the synchronous and asynchronous database classes support connection pooling, which can improve performance for applications that need to handle multiple concurrent database operations.

### Synchronous Connection Pooling

```python
from manticore_cockroachdb import Database

# Create a database with connection pooling
db = Database(
    database="example_db",
    min_pool_size=5,  # Minimum number of connections in the pool
    max_pool_size=20  # Maximum number of connections in the pool
)

# The connection pool is automatically managed
# You can use the database as normal
```

### Asynchronous Connection Pooling

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase

async def main():
    # Create a database with connection pooling
    db = AsyncDatabase(
        database="example_db",
        min_pool_size=5,  # Minimum number of connections in the pool
        max_pool_size=20  # Maximum number of connections in the pool
    )
    
    # Connect to the database
    await db.connect()
    
    try:
        # Use the database as normal
        pass
    finally:
        # Close the connection pool
        await db.close()

# Run the async function
asyncio.run(main())
```

## Custom SQL Queries

While the library provides high-level methods for common operations, you can also execute custom SQL queries when needed.

### Synchronous Custom Queries

```python
from manticore_cockroachdb import Database

db = Database(database="example_db")

# Execute a custom query
results = db.execute(
    """
    SELECT u.name, COUNT(o.id) as order_count
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.name
    HAVING COUNT(o.id) > %s
    ORDER BY order_count DESC
    LIMIT %s
    """,
    params=[5, 10]  # Parameters for the query
)

# Process the results
for row in results:
    print(f"User: {row['name']}, Orders: {row['order_count']}")
```

### Asynchronous Custom Queries

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase

async def main():
    db = AsyncDatabase(database="example_db")
    await db.connect()
    
    try:
        # Execute a custom query
        results = await db.execute(
            """
            SELECT u.name, COUNT(o.id) as order_count
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.name
            HAVING COUNT(o.id) > %s
            ORDER BY order_count DESC
            LIMIT %s
            """,
            params=[5, 10]  # Parameters for the query
        )
        
        # Process the results
        for row in results:
            print(f"User: {row['name']}, Orders: {row['order_count']}")
    finally:
        await db.close()

# Run the async function
asyncio.run(main())
```

## Transactions

Transactions allow you to group multiple database operations together, ensuring that either all operations succeed or none of them are applied.

### Synchronous Transactions

```python
from manticore_cockroachdb import Database

db = Database(database="example_db")

# Using a transaction with a context manager
with db.transaction():
    # All operations within this block are part of the same transaction
    db.insert("users", {"name": "Alice", "email": "alice@example.com"})
    db.update("accounts", {"balance": 1000}, where={"user_email": "alice@example.com"})
    
    # If any operation fails, the entire transaction is rolled back
    # If all operations succeed, the transaction is committed

# Manual transaction management
try:
    db.begin()
    db.insert("users", {"name": "Bob", "email": "bob@example.com"})
    db.update("accounts", {"balance": 500}, where={"user_email": "bob@example.com"})
    db.commit()
except Exception as e:
    db.rollback()
    print(f"Transaction failed: {e}")
```

### Asynchronous Transactions

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase

async def main():
    db = AsyncDatabase(database="example_db")
    await db.connect()
    
    try:
        # Using a transaction with a context manager
        async with db.transaction():
            # All operations within this block are part of the same transaction
            await db.insert("users", {"name": "Alice", "email": "alice@example.com"})
            await db.update("accounts", {"balance": 1000}, where={"user_email": "alice@example.com"})
            
            # If any operation fails, the entire transaction is rolled back
            # If all operations succeed, the transaction is committed
        
        # Manual transaction management
        try:
            await db.begin()
            await db.insert("users", {"name": "Bob", "email": "bob@example.com"})
            await db.update("accounts", {"balance": 500}, where={"user_email": "bob@example.com"})
            await db.commit()
        except Exception as e:
            await db.rollback()
            print(f"Transaction failed: {e}")
    finally:
        await db.close()

# Run the async function
asyncio.run(main())
```

## Working with JSON Data

CockroachDB supports JSON data types, and the Manticore CockroachDB client makes it easy to work with JSON data.

```python
import json
from manticore_cockroachdb import Database

db = Database(database="example_db")

# Create a table with a JSON column
db.create_table(
    "profiles",
    {
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "user_id": "UUID NOT NULL",
        "data": "JSONB"  # JSONB column for storing JSON data
    },
    if_not_exists=True
)

# Insert a record with JSON data
profile_id = db.insert("profiles", {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "data": json.dumps({
        "bio": "Software developer",
        "location": "New York",
        "skills": ["Python", "SQL", "JavaScript"],
        "social": {
            "twitter": "@example",
            "github": "example"
        }
    })
})

# Query JSON data
profiles = db.select(
    "profiles",
    where_clause="data->>'location' = %s",
    params=["New York"]
)

# Update JSON data
db.execute(
    """
    UPDATE profiles
    SET data = jsonb_set(data, '{skills}', %s::jsonb)
    WHERE id = %s
    """,
    params=[json.dumps(["Python", "SQL", "JavaScript", "Go"]), profile_id]
)
```

## Handling Large Result Sets

When dealing with large result sets, it's often better to process the results in chunks to avoid loading everything into memory at once.

### Synchronous Cursor

```python
from manticore_cockroachdb import Database

db = Database(database="example_db")

# Execute a query that might return a large result set
cursor = db.cursor()
cursor.execute("SELECT * FROM large_table")

# Process the results in batches
batch_size = 1000
while True:
    batch = cursor.fetchmany(batch_size)
    if not batch:
        break
    
    # Process the batch
    for row in batch:
        # Do something with the row
        pass

# Close the cursor
cursor.close()
```

### Asynchronous Cursor

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase

async def main():
    db = AsyncDatabase(database="example_db")
    await db.connect()
    
    try:
        # Execute a query that might return a large result set
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM large_table")
        
        # Process the results in batches
        batch_size = 1000
        while True:
            batch = await cursor.fetchmany(batch_size)
            if not batch:
                break
            
            # Process the batch
            for row in batch:
                # Do something with the row
                pass
        
        # Close the cursor
        await cursor.close()
    finally:
        await db.close()

# Run the async function
asyncio.run(main())
```

## Environment Variables

The Manticore CockroachDB client supports configuration through environment variables, which can be useful for managing different environments (development, testing, production).

```python
import os
from manticore_cockroachdb import Database

# Set environment variables
os.environ["DATABASE_URL"] = "postgresql://root@localhost:26257/example_db?sslmode=disable"

# Connect using the environment variable
db = Database.from_url(os.environ.get("DATABASE_URL"))

# Or use individual environment variables
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "26257"
os.environ["DB_NAME"] = "example_db"
os.environ["DB_USER"] = "root"
os.environ["DB_PASSWORD"] = ""
os.environ["DB_SSL_MODE"] = "disable"

# Connect using individual environment variables
db = Database(
    host=os.environ.get("DB_HOST"),
    port=int(os.environ.get("DB_PORT")),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    ssl_mode=os.environ.get("DB_SSL_MODE")
)
```

## Performance Tips

Here are some tips for optimizing performance when using the Manticore CockroachDB client:

1. **Use connection pooling**: For applications that need to handle multiple concurrent database operations, connection pooling can significantly improve performance.

2. **Use batch operations**: When inserting, updating, or deleting multiple records, use the batch methods (`batch_insert`, `batch_update`, `batch_delete`) instead of performing individual operations.

3. **Use transactions**: Group related operations into transactions to reduce the number of round-trips to the database.

4. **Be mindful of large result sets**: When dealing with large result sets, use cursors and process the results in batches to avoid loading everything into memory at once.

5. **Use appropriate indexes**: Make sure your tables have appropriate indexes for the queries you're running.

6. **Use prepared statements**: The library automatically uses prepared statements for parameterized queries, which can improve performance and security.

7. **Close connections**: Always close database connections when you're done with them, especially when using the asynchronous API.

8. **Monitor and optimize queries**: Use CockroachDB's built-in query monitoring tools to identify and optimize slow queries. 