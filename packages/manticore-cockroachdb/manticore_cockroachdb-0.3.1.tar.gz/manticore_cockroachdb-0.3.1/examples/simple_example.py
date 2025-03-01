"""Simple example demonstrating basic usage of Manticore CockroachDB.

This example shows:
- Connecting to a database
- Creating a table
- Performing CRUD operations
- Using transactions
"""

import logging
from manticore_cockroachdb import Database, Table
from manticore_cockroachdb.crud.exceptions import DatabaseError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run the example."""
    try:
        # Connect to database
        logger.info("Connecting to database...")
        db = Database(
            host="localhost",
            port=26257,
            database="defaultdb",
            user="root",
            password="",
            sslmode="disable",
            min_connections=2,
            max_connections=10
        )
        
        # Create a table
        logger.info("Creating users table...")
        users_schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "username": "TEXT NOT NULL UNIQUE",
            "email": "TEXT UNIQUE",
            "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
        }
        db.create_table("simple_users", users_schema, if_not_exists=True)
        
        # Create a Table instance for easier CRUD operations
        users = Table("simple_users", db=db, schema=users_schema)
        
        # Initialize the table
        logger.info("Initializing users table...")
        users.initialize()
        
        # Check if user exists before creating
        existing_user = users.find_one({"email": "john@example.com"})
        
        if existing_user:
            logger.info(f"User already exists: {existing_user}")
            user = existing_user  # Set user to the existing user
        else:
            logger.info("Creating a user...")
            try:
                user = users.create({
                    "username": "john_doe",
                    "email": "john@example.com"
                })
                logger.info(f"Created user: {user}")
            except DatabaseError as e:
                logger.error(f"Error: {e}")
        
        # Read the user
        logger.info("Reading the user...")
        retrieved_user = users.read(user["id"])
        logger.info(f"Retrieved user: {retrieved_user}")
        
        # Update the user
        logger.info("Updating the user...")
        updated_user = users.update(user["id"], {"username": "jane_doe"})
        logger.info(f"Updated user: {updated_user}")
        
        # List all users
        logger.info("Listing all users...")
        all_users = users.list()
        logger.info(f"Found {len(all_users)} users")
        
        # Using a transaction
        logger.info("Using a transaction...")
        
        def transaction_operation(conn):
            # Create two users in a transaction
            import time
            timestamp = int(time.time())
            
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO simple_users (username, email)
                    VALUES (%s, %s)
                    RETURNING *
                """, (f"user{timestamp}", f"user{timestamp}@example.com"))
                
                cur.execute("""
                    INSERT INTO simple_users (username, email)
                    VALUES (%s, %s)
                    RETURNING *
                """, (f"user{timestamp+1}", f"user{timestamp+1}@example.com"))
                
                return "Created two users in a transaction"
        
        try:
            result = db.run_in_transaction(transaction_operation)
            logger.info(f"Transaction result: {result}")
        except DatabaseError as e:
            logger.error(f"Error: {e}")
        
        # Count users
        count = users.count()
        logger.info(f"Total users: {count}")
        
        # Delete the user
        logger.info("Deleting a user...")
        deleted = users.delete(user["id"])
        logger.info(f"User deleted: {deleted}")
        
        # Batch operations
        logger.info("Performing batch operations...")
        import time
        timestamp = int(time.time())
        batch_users = [
            {"username": f"batch_user_{timestamp}_{i}", "email": f"batch{timestamp}_{i}@example.com"}
            for i in range(1, 4)
        ]
        
        try:
            created_batch = users.batch_create(batch_users)
            logger.info(f"Created {len(created_batch)} users in batch")
        except DatabaseError as e:
            logger.error(f"Error: {e}")
        
        # Close the database connection
        logger.info("Closing database connection...")
        db.close()
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 