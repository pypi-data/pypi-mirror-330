# AsyncDatabase API

The `AsyncDatabase` class provides an asynchronous interface for interacting with CockroachDB. It handles connection management, SQL execution, and transaction support using Python's async/await syntax.

## Class Documentation

::: manticore_cockroachdb.async_database.AsyncDatabase
    options:
      show_root_heading: true
      show_root_full_path: false
      show_source: true
      heading_level: 3
      members_order: source

## Usage Examples

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase

async def main():
    # Connect to database
    db = AsyncDatabase(
        host="localhost",
        port=26257,
        database="example_db",
        user="root",
        password="",
        ssl_mode="disable"
    )
    
    # Or connect using a URL
    # db = AsyncDatabase.from_url("postgresql://root@localhost:26257/example_db?sslmode=disable")
    
    # Connect to the database
    await db.connect()
    
    try:
        # Create a table
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
        
        # Insert data
        user_id = await db.insert("async_users", {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        })
        
        # Select data
        user = await db.select_one("async_users", where={"id": user_id})
        print(f"User: {user['name']}, Email: {user['email']}")
        
        # Update data
        await db.update("async_users", {"age": 31}, where={"id": user_id})
        
        # Delete data
        await db.delete("async_users", where={"id": user_id})
        
        # Execute raw SQL
        results = await db.execute("SELECT * FROM async_users WHERE age > %s", [25])
        
        # Use transactions
        async with db.transaction():
            await db.insert("async_users", {"name": "Alice", "email": "alice@example.com", "age": 25})
            await db.insert("async_users", {"name": "Bob", "email": "bob@example.com", "age": 28})
            
    finally:
        # Close the connection
        await db.close()

# Run the async function
asyncio.run(main())
``` 