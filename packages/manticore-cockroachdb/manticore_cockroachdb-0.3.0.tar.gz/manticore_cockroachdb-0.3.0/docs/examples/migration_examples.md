# Migration Examples

This page provides practical examples of using the migration features of the Manticore CockroachDB client. These examples demonstrate how to manage database schema changes effectively.

## Synchronous Migrations

This example shows how to create and apply migrations using the synchronous API:

```python
import os
from manticore_cockroachdb import Database, Migration

def sync_migration_example():
    # Connect to database
    db = Database(database="testdb", host="localhost")
    db.connect()
    
    try:
        # Create migration directory if it doesn't exist
        migrations_dir = "migrations"
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir)
        
        # Create migration files
        Migration.create_migration(
            "001_create_users_table",
            """
            CREATE TABLE users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """,
            """
            DROP TABLE users;
            """,
            directory=migrations_dir
        )
        
        Migration.create_migration(
            "002_add_age_column",
            """
            ALTER TABLE users ADD COLUMN age INTEGER;
            """,
            """
            ALTER TABLE users DROP COLUMN age;
            """,
            directory=migrations_dir
        )
        
        # Load migrations
        migrations = Migration.load_migrations(migrations_dir)
        print("Loaded {} migrations".format(len(migrations)))
        
        # Print migration details
        for m in migrations:
            print("  Version {}: {}".format(m.version, m.description))
        
        # Apply all migrations
        applied = Migration.apply_migrations(db, migrations)
        print("Applied {} migrations".format(len(applied)))
        
        # Insert test data
        db.execute(
            "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
            ("testuser", "test@example.com", 30)
        )
        
        # Query the data
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            for user in users:
                print("User: {}, Email: {}, Age: {}".format(
                    user["username"], user["email"], user["age"]
                ))
        
        # Check current migration version
        version = Migration.get_current_version(db)
        print("Current migration version: {}".format(version))
        
        # Roll back the last migration
        rolled_back = Migration.rollback_migration(db, migrations[-1])
        print("Rolled back migration: {}".format(rolled_back.version))
        
        # Verify the age column is gone
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            for user in users:
                print("User after rollback: {}, Email: {}".format(
                    user["username"], user["email"]
                ))
                # Age column should no longer exist
        
    finally:
        # Clean up
        try:
            db.execute("DROP TABLE IF EXISTS migrations")
            db.execute("DROP TABLE IF EXISTS users")
        except Exception as e:
            print("Cleanup error: {}".format(e))
        db.close()

if __name__ == "__main__":
    sync_migration_example()
```

## Asynchronous Migrations

This example shows how to create and apply migrations using the asynchronous API:

```python
import os
import asyncio
from manticore_cockroachdb import AsyncDatabase, AsyncMigration

async def async_migration_example():
    # Connect to database
    db = AsyncDatabase(database="testdb", host="localhost")
    await db.connect()
    
    try:
        # Create migration directory if it doesn't exist
        migrations_dir = "async_migrations"
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir)
        
        # Create migration files
        await AsyncMigration.create_migration(
            "001_create_products_table",
            """
            CREATE TABLE products (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """,
            """
            DROP TABLE products;
            """,
            directory=migrations_dir
        )
        
        await AsyncMigration.create_migration(
            "002_add_description_column",
            """
            ALTER TABLE products ADD COLUMN description TEXT;
            """,
            """
            ALTER TABLE products DROP COLUMN description;
            """,
            directory=migrations_dir
        )
        
        await AsyncMigration.create_migration(
            "003_add_category_column",
            """
            ALTER TABLE products ADD COLUMN category TEXT NOT NULL DEFAULT 'Uncategorized';
            """,
            """
            ALTER TABLE products DROP COLUMN category;
            """,
            directory=migrations_dir
        )
        
        # Load migrations
        migrations = await AsyncMigration.load_migrations(migrations_dir)
        print("Loaded {} migrations".format(len(migrations)))
        
        # Print migration details
        for m in migrations:
            print("  Version {}: {}".format(m.version, m.description))
        
        # Apply all migrations
        applied = await AsyncMigration.apply_migrations(db, migrations)
        print("Applied {} migrations".format(len(applied)))
        
        # Insert test data
        async with db.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO products (name, price, description, category) VALUES (%s, %s, %s, %s)",
                ("Laptop", 1299.99, "High-performance laptop", "Electronics")
            )
            
            await cursor.execute(
                "INSERT INTO products (name, price, description, category) VALUES (%s, %s, %s, %s)",
                ("Headphones", 199.99, "Noise-cancelling headphones", "Audio")
            )
        
        # Query the data
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM products")
            products = await cursor.fetchall()
            for product in products:
                print("Product: {}, Price: ${:.2f}, Category: {}, Description: {}".format(
                    product["name"], product["price"], product["category"], product["description"]
                ))
        
        # Check current migration version
        version = await AsyncMigration.get_current_version(db)
        print("Current migration version: {}".format(version))
        
        # Roll back the last migration
        rolled_back = await AsyncMigration.rollback_migration(db, migrations[-1])
        print("Rolled back migration: {}".format(rolled_back.version))
        
        # Roll back another migration
        rolled_back = await AsyncMigration.rollback_migration(db, migrations[-2])
        print("Rolled back migration: {}".format(rolled_back.version))
        
        # Verify columns are gone
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM products")
            products = await cursor.fetchall()
            for product in products:
                print("Product after rollbacks: {}, Price: ${:.2f}".format(
                    product["name"], product["price"]
                ))
                # Description and category columns should no longer exist
        
    finally:
        # Clean up
        try:
            await db.execute("DROP TABLE IF EXISTS migrations")
            await db.execute("DROP TABLE IF EXISTS products")
        except Exception as e:
            print("Cleanup error: {}".format(e))
        await db.close()

if __name__ == "__main__":
    asyncio.run(async_migration_example())
```

## Migration with Transactions

This example demonstrates how to use transactions with migrations for atomic schema changes:

```python
import os
from manticore_cockroachdb import Database, Migration

def transaction_migration_example():
    # Connect to database
    db = Database(database="testdb", host="localhost")
    db.connect()
    
    try:
        # Create migration directory
        migrations_dir = "transaction_migrations"
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir)
        
        # Create a migration with multiple operations in a transaction
        Migration.create_migration(
            "001_create_related_tables",
            """
            -- Create categories table
            CREATE TABLE categories (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL UNIQUE,
                description TEXT
            );
            
            -- Create items table with foreign key
            CREATE TABLE items (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                category_id UUID NOT NULL REFERENCES categories(id),
                price DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            
            -- Create index for faster lookups
            CREATE INDEX items_category_idx ON items(category_id);
            """,
            """
            DROP TABLE IF EXISTS items;
            DROP TABLE IF EXISTS categories;
            """,
            directory=migrations_dir
        )
        
        # Load and apply migrations
        migrations = Migration.load_migrations(migrations_dir)
        applied = Migration.apply_migrations(db, migrations)
        print("Applied {} migrations".format(len(applied)))
        
        # Insert test data using transactions
        def insert_test_data(conn):
            with conn.cursor() as cur:
                # Insert categories
                cur.execute(
                    "INSERT INTO categories (name, description) VALUES (%s, %s) RETURNING id",
                    ("Electronics", "Electronic devices and gadgets")
                )
                electronics_id = cur.fetchone()["id"]
                
                cur.execute(
                    "INSERT INTO categories (name, description) VALUES (%s, %s) RETURNING id",
                    ("Books", "Books and publications")
                )
                books_id = cur.fetchone()["id"]
                
                # Insert items
                items = [
                    ("Smartphone", electronics_id, 699.99),
                    ("Tablet", electronics_id, 349.99),
                    ("Novel", books_id, 14.99),
                    ("Textbook", books_id, 79.99)
                ]
                
                for name, category_id, price in items:
                    cur.execute(
                        "INSERT INTO items (name, category_id, price) VALUES (%s, %s, %s)",
                        (name, category_id, price)
                    )
                
                return {
                    "electronics_id": electronics_id,
                    "books_id": books_id
                }
        
        # Run in transaction
        result = db.run_in_transaction(insert_test_data)
        print("Inserted test data with category IDs: {}".format(result))
        
        # Query the data with a join
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT i.name as item_name, i.price, c.name as category_name
                FROM items i
                JOIN categories c ON i.category_id = c.id
                ORDER BY c.name, i.price DESC
            """)
            
            items = cursor.fetchall()
            print("\nItems by category:")
            for item in items:
                print("  {} ({}): ${:.2f}".format(
                    item["item_name"], item["category_name"], item["price"]
                ))
        
    finally:
        # Clean up
        try:
            db.execute("DROP TABLE IF EXISTS items")
            db.execute("DROP TABLE IF EXISTS categories")
            db.execute("DROP TABLE IF EXISTS migrations")
        except Exception as e:
            print("Cleanup error: {}".format(e))
        db.close()

if __name__ == "__main__":
    transaction_migration_example()
```

## Migration Status and History

This example shows how to check migration status and history:

```python
import os
from manticore_cockroachdb import Database, Migration

def migration_status_example():
    # Connect to database
    db = Database(database="testdb", host="localhost")
    db.connect()
    
    try:
        # Create migration directory
        migrations_dir = "status_migrations"
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir)
        
        # Create several migrations
        for i in range(1, 6):
            version = f"{i:03d}"
            Migration.create_migration(
                f"{version}_migration_{i}",
                f"-- Migration {i} up\nCREATE TABLE IF NOT EXISTS table_{i} (id SERIAL PRIMARY KEY, name TEXT);",
                f"-- Migration {i} down\nDROP TABLE IF EXISTS table_{i};",
                directory=migrations_dir
            )
        
        # Load migrations
        migrations = Migration.load_migrations(migrations_dir)
        print("Loaded {} migrations".format(len(migrations)))
        
        # Apply only the first 3 migrations
        applied = Migration.apply_migrations(db, migrations[:3])
        print("Applied {} migrations".format(len(applied)))
        
        # Check current version
        version = Migration.get_current_version(db)
        print("Current migration version: {}".format(version))
        
        # Get migration history
        history = Migration.get_migration_history(db)
        print("\nMigration history:")
        for entry in history:
            print("  Version: {}, Applied at: {}, Description: {}".format(
                entry["version"], entry["applied_at"], entry["description"]
            ))
        
        # Check pending migrations
        pending = Migration.get_pending_migrations(db, migrations)
        print("\nPending migrations:")
        for m in pending:
            print("  Version: {}, Description: {}".format(m.version, m.description))
        
        # Apply one more migration
        applied = Migration.apply_migrations(db, [pending[0]])
        print("\nApplied 1 more migration: {}".format(applied[0].version))
        
        # Check status again
        version = Migration.get_current_version(db)
        print("Current migration version: {}".format(version))
        
        # Roll back to version 002
        target_version = "002"
        rolled_back = Migration.rollback_to_version(db, migrations, target_version)
        print("\nRolled back to version {}, migrations rolled back: {}".format(
            target_version, len(rolled_back)
        ))
        
        # Verify current version
        version = Migration.get_current_version(db)
        print("Current migration version after rollback: {}".format(version))
        
    finally:
        # Clean up
        try:
            for i in range(1, 6):
                db.execute(f"DROP TABLE IF EXISTS table_{i}")
            db.execute("DROP TABLE IF EXISTS migrations")
        except Exception as e:
            print("Cleanup error: {}".format(e))
        db.close()

if __name__ == "__main__":
    migration_status_example() 