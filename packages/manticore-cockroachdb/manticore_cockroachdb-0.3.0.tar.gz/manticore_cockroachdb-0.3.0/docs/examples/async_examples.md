# Async Examples

This page provides practical examples of using the asynchronous API of the Manticore CockroachDB client. These examples demonstrate common patterns and best practices for working with the library in async environments.

## Basic CRUD Operations

This example shows how to perform basic CRUD operations using the asynchronous API:

```python
import asyncio
import uuid
from manticore_cockroachdb import AsyncDatabase, AsyncTable

async def async_crud_example():
    # Connect to database
    db = AsyncDatabase(database="testdb", host="localhost")
    await db.connect()
    
    try:
        # Create a products table
        products = AsyncTable(
            "products",
            db=db,
            schema={
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "name": "TEXT NOT NULL",
                "price": "DECIMAL(10,2) NOT NULL",
                "stock": "INTEGER NOT NULL DEFAULT 0",
                "active": "BOOLEAN NOT NULL DEFAULT TRUE"
            }
        )
        
        # Initialize the table
        await products.initialize()
        
        # Create a product
        product = await products.create({
            "name": "Smartphone",
            "price": 799.99,
            "stock": 50
        })
        print(f"Created product: {product}")
        
        # Read the product
        retrieved = await products.read(product["id"])
        print(f"Retrieved product: {retrieved}")
        
        # Update the product
        updated = await products.update(product["id"], {
            "price": 749.99,
            "stock": 45
        })
        print(f"Updated product: {updated}")
        
        # List all products
        all_products = await products.list()
        print(f"All products: {all_products}")
        
        # Delete the product
        deleted = await products.delete(product["id"])
        print(f"Product deleted: {deleted}")
        
    finally:
        # Close the database connection
        await db.close()

asyncio.run(async_crud_example())
```

## Working with Transactions

This example demonstrates how to use transactions with the asynchronous API:

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase, AsyncTable

async def transaction_example():
    # Connect to database
    db = AsyncDatabase(database="testdb", host="localhost")
    await db.connect()
    
    try:
        # Create tables
        accounts = AsyncTable(
            "accounts",
            db=db,
            schema={
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "owner": "TEXT NOT NULL",
                "balance": "DECIMAL(12,2) NOT NULL"
            }
        )
        await accounts.initialize()
        
        # Create initial accounts
        account1 = await accounts.create({
            "owner": "Alice",
            "balance": 1000.00
        })
        
        account2 = await accounts.create({
            "owner": "Bob",
            "balance": 500.00
        })
        
        # Perform a transfer using a transaction
        async def transfer_funds(conn):
            amount = 200.00
            
            # Deduct from account1
            async with conn.cursor() as cur:
                await cur.execute(
                    "UPDATE accounts SET balance = balance - %s WHERE id = %s RETURNING *",
                    (amount, account1["id"])
                )
                sender = await cur.fetchone()
                
                # Add to account2
                await cur.execute(
                    "UPDATE accounts SET balance = balance + %s WHERE id = %s RETURNING *",
                    (amount, account2["id"])
                )
                recipient = await cur.fetchone()
                
                return {
                    "sender": sender,
                    "recipient": recipient,
                    "amount": amount
                }
        
        # Run the transfer in a transaction
        result = await db.run_in_transaction(transfer_funds)
        print(f"Transfer completed: {result}")
        
        # Verify the new balances
        updated_account1 = await accounts.read(account1["id"])
        updated_account2 = await accounts.read(account2["id"])
        
        print(f"{updated_account1['owner']}'s balance: {updated_account1['balance']}")
        print(f"{updated_account2['owner']}'s balance: {updated_account2['balance']}")
        
    finally:
        # Clean up
        await db.drop_table("accounts")
        await db.close()

asyncio.run(transaction_example())
```

## Batch Operations

This example shows how to perform batch operations efficiently:

```python
import asyncio
import random
from manticore_cockroachdb import AsyncDatabase, AsyncTable

async def batch_operations_example():
    # Connect to database
    db = AsyncDatabase(database="testdb", host="localhost")
    await db.connect()
    
    try:
        # Create a sensors table
        sensors = AsyncTable(
            "sensors",
            db=db,
            schema={
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "location": "TEXT NOT NULL",
                "type": "TEXT NOT NULL",
                "reading": "FLOAT NOT NULL",
                "timestamp": "TIMESTAMP DEFAULT NOW()"
            }
        )
        await sensors.initialize()
        
        # Generate sensor data
        sensor_data = []
        locations = ["kitchen", "living_room", "bedroom", "bathroom", "garage"]
        types = ["temperature", "humidity", "pressure", "light"]
        
        for _ in range(20):
            sensor_data.append({
                "location": random.choice(locations),
                "type": random.choice(types),
                "reading": round(random.uniform(0, 100), 2)
            })
        
        # Insert all records in a batch
        inserted = await sensors.batch_create(sensor_data)
        print(f"Inserted {len(inserted)} sensor readings")
        
        # Query data - temperature sensors with high readings
        high_temps = await sensors.list(
            where={"type": "temperature"},
            order_by="reading DESC",
            limit=5
        )
        
        print("\nHighest temperature readings:")
        for reading in high_temps:
            print(f"Location: {reading['location']}, Reading: {reading['reading']}°C")
        
        # Update multiple records in batch
        # For example, adjust all humidity readings
        humidity_readings = await sensors.list(where={"type": "humidity"})
        for reading in humidity_readings:
            reading["reading"] = round(reading["reading"] * 0.95, 2)  # Adjust by 5%
        
        updated = await sensors.batch_update(humidity_readings)
        print(f"\nUpdated {len(updated)} humidity readings")
        
    finally:
        # Clean up
        await db.drop_table("sensors")
        await db.close()

asyncio.run(batch_operations_example())
```

## Using Context Managers

This example demonstrates how to use async context managers for cleaner code:

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase, AsyncTable

async def context_manager_example():
    # Use database as context manager
    async with AsyncDatabase(database="testdb", host="localhost") as db:
        # Use table as context manager
        async with AsyncTable(
            "notes",
            db=db,
            schema={
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "title": "TEXT NOT NULL",
                "content": "TEXT",
                "created_at": "TIMESTAMP DEFAULT NOW()"
            }
        ) as notes:
            # Table is automatically initialized
            
            # Create notes
            await notes.create({
                "title": "Shopping List",
                "content": "Milk, Eggs, Bread"
            })
            
            await notes.create({
                "title": "Meeting Notes",
                "content": "Discuss project timeline and resource allocation"
            })
            
            # List all notes
            all_notes = await notes.list(order_by="created_at DESC")
            
            print("Notes:")
            for note in all_notes:
                print(f"- {note['title']}: {note['content']}")
        
        # Clean up
        await db.drop_table("notes")
        # Connection is automatically closed when exiting the context

asyncio.run(context_manager_example())
```

## Error Handling

This example shows proper error handling with the async API:

```python
import asyncio
from manticore_cockroachdb import AsyncDatabase, AsyncTable
from psycopg.errors import UniqueViolation, ForeignKeyViolation

async def error_handling_example():
    # Connect to database
    db = AsyncDatabase(database="testdb", host="localhost")
    await db.connect()
    
    try:
        # Create a users table
        users = AsyncTable(
            "users_example",
            db=db,
            schema={
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "username": "TEXT NOT NULL UNIQUE",  # Unique constraint
                "email": "TEXT NOT NULL"
            }
        )
        await users.initialize()
        
        # Create a user
        try:
            user = await users.create({
                "username": "johndoe",
                "email": "john@example.com"
            })
            print(f"Created user: {user['username']}")
            
            # Try to create another user with the same username (will fail)
            duplicate_user = await users.create({
                "username": "johndoe",  # Same username
                "email": "another@example.com"
            })
            
        except UniqueViolation as e:
            print(f"Couldn't create duplicate user: {e}")
            
            # Handle the error and try a different username
            try:
                alternate_user = await users.create({
                    "username": "johndoe2",  # Different username
                    "email": "another@example.com"
                })
                print(f"Created alternative user: {alternate_user['username']}")
                
            except Exception as e2:
                print(f"Failed to create alternative user: {e2}")
        
        # List all successful users
        all_users = await users.list()
        print(f"Total users: {len(all_users)}")
        for user in all_users:
            print(f"- {user['username']}: {user['email']}")
            
    except Exception as e:
        print(f"Unexpected error: {e}")
        
    finally:
        # Clean up
        await db.drop_table("users_example")
        await db.close()

asyncio.run(error_handling_example())
``` 