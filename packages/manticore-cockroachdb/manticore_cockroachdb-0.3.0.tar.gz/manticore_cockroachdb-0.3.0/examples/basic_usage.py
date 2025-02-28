#!/usr/bin/env python3
"""Basic usage examples for the Manticore CockroachDB client.

This example demonstrates the core functionality of the library:
1. Connecting to a CockroachDB database
2. Creating tables
3. Performing CRUD operations
4. Using transactions
5. Working with Table abstraction

Prerequisites:
- A running CockroachDB server
- The manticore-cockroachdb library installed
"""

import os
import uuid
import logging
from decimal import Decimal

from manticore_cockroachdb.database import Database
from manticore_cockroachdb.crud.table import Table

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run the example."""
    # Connect to database - either from environment or defaults
    database_url = os.environ.get("DATABASE_URL")
    
    if database_url:
        logger.info("Connecting to database using DATABASE_URL")
        db = Database.from_url(database_url)
    else:
        logger.info("Connecting to local CockroachDB instance")
        db = Database(database="example_db")
    
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
        
        # Create users table
        logger.info("Creating users table")
        db.create_table("example_users", users_schema, if_not_exists=True)
        
        # Create a Table instance for more convenient operations
        users = Table("example_users", db=db)
        
        # Create a user
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "balance": Decimal("100.50")
        }
        
        logger.info("Creating user: %s", user_data["name"])
        user = users.create(user_data)
        logger.info("Created user: %s with ID: %s", user["name"], user["id"])
        
        # Read the user
        retrieved_user = users.read(user["id"])
        logger.info("Retrieved user: %s", retrieved_user["name"])
        
        # Update the user
        logger.info("Updating user balance")
        updated_user = users.update(user["id"], {"balance": Decimal("150.75")})
        logger.info("Updated balance: %s", updated_user["balance"])
        
        # List all users
        all_users = users.list()
        logger.info("Total users: %s", len(all_users))
        
        # Filter users
        active_users = users.list(where={"active": True})
        logger.info("Active users: %s", len(active_users))
        
        # Count users
        user_count = users.count()
        logger.info("User count: %s", user_count)
        
        # Batch operations
        batch_users = [
            {"name": "Batch User {0}".format(i), "email": "batch{0}@example.com".format(i), "age": 20 + i}
            for i in range(1, 4)
        ]
        
        logger.info("Creating batch of users")
        created_batch = users.batch_create(batch_users)
        logger.info("Created %s users in batch", len(created_batch))
        
        # Update batch
        for user in created_batch:
            user["age"] += 1
        
        logger.info("Updating batch of users")
        updated_batch = users.batch_update(created_batch)
        logger.info("Updated %s users in batch", len(updated_batch))
        
        # Transaction example
        logger.info("Running transaction example")
        
        def transfer_money(conn):
            """Transfer money between users."""
            # Simulate money transfer in a transaction
            with conn.cursor() as cur:
                # Deduct from John
                cur.execute(
                    "UPDATE example_users SET balance = balance - 50.00 WHERE email = %s",
                    ("john@example.com",)
                )
                
                # Add to first batch user
                cur.execute(
                    "UPDATE example_users SET balance = balance + 50.00 WHERE email = %s",
                    ("batch1@example.com",)
                )
                
                # Get updated balances
                cur.execute(
                    "SELECT name, balance FROM example_users WHERE email IN (%s, %s)",
                    ("john@example.com", "batch1@example.com")
                )
                return cur.fetchall()
        
        # Run the transfer in a transaction
        result = db.run_in_transaction(transfer_money)
        for user in result:
            logger.info("User %s has balance: %s", user["name"], user["balance"])
        
        # Clean up - delete some users
        logger.info("Deleting batch users")
        for user in created_batch:
            deleted = users.delete(user["id"])
            logger.info("Deleted user %s: %s", user["name"], deleted)
        
        # Use Table as a context manager for another operation
        logger.info("Using Table as a context manager")
        with Table("example_users", db=db) as users_ctx:
            user = users_ctx.read(retrieved_user["id"])
            logger.info("Retrieved user with context manager: %s", user["name"])
        
    finally:
        # Clean up
        logger.info("Dropping example_users table")
        db.drop_table("example_users", if_exists=True)
        
        # Close database connection
        logger.info("Closing database connection")
        db.close()


if __name__ == "__main__":
    main() 