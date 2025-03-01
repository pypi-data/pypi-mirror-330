"""Async example demonstrating basic usage of Manticore CockroachDB.

This example shows:
- Connecting to a database asynchronously
- Creating a table
- Performing CRUD operations with async/await
- Using async transactions
"""

import asyncio
import logging
from manticore_cockroachdb import AsyncDatabase, AsyncTable
from manticore_cockroachdb.crud.exceptions import DatabaseError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Run the async example."""
    try:
        # Connect to database
        logger.info("Connecting to database...")
        db = AsyncDatabase(
            host="localhost",
            port=26257,
            database="defaultdb",
            user="root",
            password="",
            min_connections=2,
            max_connections=10
        )
        await db.connect()
        
        try:
            # Create a table
            logger.info("Creating users table...")
            users_schema = {
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "username": "TEXT NOT NULL UNIQUE",
                "email": "TEXT UNIQUE",
                "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
            }
            await db.create_table("async_users", users_schema, if_not_exists=True)
            
            # Create a Table instance for easier CRUD operations
            users = AsyncTable("async_users", db=db, schema=users_schema)
            
            # Initialize the table
            logger.info("Initializing users table...")
            await users.initialize()
            
            # Check if user exists before creating
            logger.info("Checking if user exists...")
            existing_user = await db.execute(
                "SELECT * FROM async_users WHERE email = %s",
                ("async_john@example.com",)
            )
            
            if existing_user:
                logger.info(f"User already exists: {existing_user[0]}")
                user = existing_user[0]  # Use the existing user
            else:
                # Create a user
                logger.info("Creating a new user...")
                try:
                    user = await users.create({
                        "username": "async_john",
                        "email": "async_john@example.com"
                    })
                    logger.info(f"Created user: {user}")
                except DatabaseError as e:
                    if "duplicate key value" in str(e):
                        logger.info("User already exists (caught duplicate key error)")
                        # Get the existing user
                        existing_user = await db.execute(
                            "SELECT * FROM async_users WHERE email = %s",
                            ("async_john@example.com",)
                        )
                        user = existing_user[0]
                    else:
                        raise
            
            # Read the user
            logger.info("Reading the user...")
            retrieved_user = await users.read(user["id"])
            logger.info(f"Retrieved user: {retrieved_user}")
            
            # Update the user
            logger.info("Updating the user...")
            updated_user = await users.update(user["id"], {"username": "async_jane"})
            logger.info(f"Updated user: {updated_user}")
            
            # List all users
            logger.info("Listing all users...")
            all_users = await users.list()
            logger.info(f"Found {len(all_users)} users")
            
            # Using a transaction
            logger.info("Using a transaction...")
            
            async def transaction_operation(conn):
                # Create two users in a transaction
                import time
                timestamp = int(time.time())
                
                async with conn.cursor() as cur:
                    await cur.execute("""
                        INSERT INTO async_users (username, email)
                        VALUES (%s, %s)
                        ON CONFLICT (username) DO NOTHING
                        RETURNING *
                    """, (f"async_user{timestamp}_1", f"async_user{timestamp}_1@example.com"))
                    
                    await cur.execute("""
                        INSERT INTO async_users (username, email)
                        VALUES (%s, %s)
                        ON CONFLICT (username) DO NOTHING
                        RETURNING *
                    """, (f"async_user{timestamp}_2", f"async_user{timestamp}_2@example.com"))
                    
                    return "Created two users in a transaction"
            
            result = await db.run_in_transaction(transaction_operation)
            logger.info(f"Transaction result: {result}")
            
            # Count users
            count = await users.count()
            logger.info(f"Total users: {count}")
            
            # Delete the user
            logger.info("Deleting a user...")
            deleted = await users.delete(user["id"])
            logger.info(f"User deleted: {deleted}")
            
            # Batch operations
            logger.info("Performing batch operations...")
            import time
            timestamp = int(time.time())
            batch_users = [
                {"username": f"async_batch_{timestamp}_{i}", "email": f"async_batch{timestamp}_{i}@example.com"}
                for i in range(1, 4)
            ]
            created_batch = await users.batch_create(batch_users)
            logger.info(f"Created {len(created_batch)} users in batch")
            
        finally:
            # Close the database connection
            logger.info("Closing database connection...")
            await db.close()
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main()) 