#!/usr/bin/env python3
"""Async usage examples for the Manticore CockroachDB client.

This example demonstrates the asynchronous functionality of the library:
1. Connecting to a CockroachDB database asynchronously 
2. Creating tables
3. Performing async CRUD operations
4. Using async transactions
5. Working with AsyncTable abstraction

Prerequisites:
- A running CockroachDB server
- The manticore-cockroachdb library installed
"""

import os
import uuid
import asyncio
import logging
from decimal import Decimal

from manticore_cockroachdb.async_database import AsyncDatabase
from manticore_cockroachdb.crud.async_table import AsyncTable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Run the async example."""
    # Connect to database - either from environment or defaults
    database_url = os.environ.get("DATABASE_URL")
    
    if database_url:
        logger.info("Connecting to database using DATABASE_URL")
        db = AsyncDatabase.from_url(database_url)
    else:
        logger.info("Connecting to local CockroachDB instance")
        db = AsyncDatabase(database="example_db")
    
    # Connect to database
    await db.connect()
    
    try:
        # Define users table schema
        users_schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL",
            "age": "INTEGER",
            "active": "BOOLEAN DEFAULT TRUE",
            "balance": "DECIMAL(10,2) DEFAULT 0.00",
        }
        
        # Create table
        logger.info("Creating async_example_users table")
        await db.create_table("async_example_users", users_schema, if_not_exists=True)
        
        # Create a Table instance for more convenient operations
        users = AsyncTable("async_example_users", db=db)
        await users.initialize()
        
        # Create a user
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "balance": Decimal("100.50")
        }
        
        logger.info("Creating user: %s", user_data["name"])
        user = await users.create(user_data)
        logger.info("Created user: %s with ID: %s", user["name"], user["id"])
        
        # Read the user
        retrieved_user = await users.read(user["id"])
        logger.info("Retrieved user: %s", retrieved_user["name"])
        
        # Update the user
        logger.info("Updating user balance")
        updated_user = await users.update(user["id"], {"balance": Decimal("150.75")})
        logger.info("Updated balance: %s", updated_user["balance"])
        
        # List all users
        all_users = await users.list()
        logger.info("Total users: %s", len(all_users))
        
        # Filter users
        active_users = await users.list(where={"active": True})
        logger.info("Active users: %s", len(active_users))
        
        # Count users
        user_count = await users.count()
        logger.info("User count: %s", user_count)
        
        # Batch operations
        batch_users = [
            {"name": "Batch User {0}".format(i), "email": "batch{0}@example.com".format(i), "age": 20 + i}
            for i in range(1, 4)
        ]
        
        logger.info("Creating batch of users")
        created_batch = await users.batch_create(batch_users)
        logger.info("Created %s users in batch", len(created_batch))
        
        # Update batch
        for user in created_batch:
            user["age"] += 1
        
        logger.info("Updating batch of users")
        updated_batch = await users.batch_update(created_batch)
        logger.info("Updated %s users in batch", len(updated_batch))
        
        # Transaction example
        logger.info("Running transaction example")
        
        async def transfer_money(conn):
            """Transfer money between users."""
            # Simulate money transfer in a transaction
            async with conn.cursor() as cur:
                # Deduct from John
                await cur.execute(
                    "UPDATE async_example_users SET balance = balance - 50.00 WHERE email = %s",
                    ("john@example.com",)
                )
                
                # Add to first batch user
                await cur.execute(
                    "UPDATE async_example_users SET balance = balance + 50.00 WHERE email = %s",
                    ("batch1@example.com",)
                )
                
                # Get updated balances
                await cur.execute(
                    "SELECT name, balance FROM async_example_users WHERE email IN (%s, %s)",
                    ("john@example.com", "batch1@example.com")
                )
                return await cur.fetchall()
        
        # Run the transfer in a transaction
        result = await db.run_in_transaction(transfer_money)
        for user in result:
            logger.info("User %s has balance: %s", user["name"], user["balance"])
        
        # Clean up - delete some users
        logger.info("Deleting batch users")
        for user in created_batch:
            deleted = await users.delete(user["id"])
            logger.info("Deleted user %s: %s", user["name"], deleted)
        
        # Use AsyncTable as a context manager for another operation
        logger.info("Using AsyncTable as a context manager")
        async with AsyncTable("async_example_users", db=db) as users_ctx:
            user = await users_ctx.read(retrieved_user["id"])
            logger.info("Retrieved user with context manager: %s", user["name"])
        
    finally:
        # Clean up
        logger.info("Dropping async_example_users table")
        await db.drop_table("async_example_users", if_exists=True)
        
        # Close database connection
        logger.info("Closing database connection")
        await db.close()


if __name__ == "__main__":
    asyncio.run(main()) 