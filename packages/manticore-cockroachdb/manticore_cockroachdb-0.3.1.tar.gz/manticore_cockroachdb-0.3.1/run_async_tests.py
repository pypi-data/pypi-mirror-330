#!/usr/bin/env python3
"""Script to run async tests directly using asyncio."""

import asyncio
import os
import tempfile
import shutil
import uuid
import sys
from pathlib import Path
from decimal import Decimal

from manticore_cockroachdb.async_database import AsyncDatabase
from manticore_cockroachdb.async_migration import AsyncMigrator
from manticore_cockroachdb.crud.async_table import AsyncTable

async def setup_db():
    """Create async test database."""
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        database = AsyncDatabase.from_url(database_url)
    else:
        database = AsyncDatabase(database="test_db")
    
    await database.connect()
    return database

async def setup_migrator(db):
    """Create async migrator instance."""
    temp_dir = tempfile.mkdtemp()
    print(f"Created temporary directory: {temp_dir}")
    migrator = AsyncMigrator(db, migrations_dir=temp_dir)
    await migrator.initialize()
    return migrator, temp_dir

async def cleanup(db, temp_dir):
    """Clean up resources."""
    try:
        await db.execute("DROP TABLE IF EXISTS _migrations")
        await db.execute("DROP TABLE IF EXISTS async_test_table")
        await db.execute("DROP TABLE IF EXISTS async_users")
        await db.execute("DROP TABLE IF EXISTS async_posts")
        await db.execute("DROP TABLE IF EXISTS async_users_table")
        await db.execute("DROP TABLE IF EXISTS async_batch_table")
        await db.execute("DROP TABLE IF EXISTS async_transaction_table")
    except Exception as e:
        print(f"Error during cleanup: {e}")
    
    await db.close()
    shutil.rmtree(temp_dir)

async def test_create_migration(migrator, migrations_dir):
    """Test creating a migration."""
    # Create a migration
    migration_name = "create_test_table"
    await migrator.create_migration(
        migration_name,
        "CREATE TABLE async_test_table (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_test_table"
    )
    
    # Check that the files were created
    print(f"Looking for migration files in {migrations_dir}")
    migration_files = [f for f in os.listdir(migrations_dir) if migration_name in f]
    print(f"Found migration files: {migration_files}")
    assert migration_files, f"No migration files found for {migration_name}"
    
    # Check for up migration file (V*.sql)
    up_files = [f for f in migration_files if f.startswith('V')]
    assert up_files, "No up migration file found"
    up_path = os.path.join(migrations_dir, up_files[0])
    assert os.path.exists(up_path), f"Up migration file {up_path} does not exist"
    
    # Check for down migration file (U*.sql)
    down_files = [f for f in migration_files if f.startswith('U')]
    assert down_files, "No down migration file found"
    down_path = os.path.join(migrations_dir, down_files[0])
    assert os.path.exists(down_path), f"Down migration file {down_path} does not exist"
    
    # Check file content
    with open(up_path, "r") as f:
        content = f.read()
        print(f"Up migration file content:\n{content}")
        assert "CREATE TABLE async_test_table" in content, "CREATE statement not found in up migration"
    
    with open(down_path, "r") as f:
        content = f.read()
        print(f"Down migration file content:\n{content}")
        assert "DROP TABLE async_test_table" in content, "DROP statement not found in down migration"
    
    print("✅ test_create_migration passed")

async def test_load_migrations(migrator, migrations_dir):
    """Test loading migrations."""
    # Create multiple migrations
    await migrator.create_migration(
        "create_users",
        "CREATE TABLE async_users (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL)",
        "DROP TABLE async_users"
    )
    
    await migrator.create_migration(
        "create_posts",
        "CREATE TABLE async_posts (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), title TEXT NOT NULL)",
        "DROP TABLE async_posts"
    )
    
    # Load migrations
    migrations = await migrator.load_migrations()
    
    # Check that migrations were loaded
    assert len(migrations) >= 2, f"Expected at least 2 migrations, got {len(migrations)}"
    
    # Check migration order
    assert migrations[0].version < migrations[1].version, "Migrations not ordered by version"
    
    print("✅ test_load_migrations passed")

async def test_async_table_operations(db):
    """Test async table operations."""
    # Create a table
    table = AsyncTable(
        "async_users_table",
        db=db,
        schema={
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL",
            "age": "INTEGER",
            "active": "BOOLEAN DEFAULT TRUE",
        }
    )
    await table.initialize()
    
    # Create a user
    user = await table.create({
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    })
    
    assert user["name"] == "John Doe"
    assert user["email"] == "john@example.com"
    assert user["age"] == 30
    assert user["active"] is True
    assert "id" in user
    
    # Read the user
    retrieved = await table.read(user["id"])
    assert retrieved["id"] == user["id"]
    assert retrieved["name"] == "John Doe"
    
    # Update the user
    updated = await table.update(user["id"], {
        "age": 31,
        "active": False
    })
    
    assert updated["id"] == user["id"]
    assert updated["name"] == "John Doe"  # Unchanged
    assert updated["email"] == "john@example.com"  # Unchanged
    assert updated["age"] == 31  # Changed
    assert updated["active"] is False  # Changed
    
    # List all users
    all_users = await table.list()
    assert len(all_users) >= 1
    
    # Delete the user
    result = await table.delete(user["id"])
    assert result is True
    
    # Verify deletion
    retrieved = await table.read(user["id"])
    assert retrieved is None
    
    print("✅ test_async_table_operations passed")

async def test_async_batch_operations(db):
    """Test async batch operations."""
    # Create a table
    table = AsyncTable(
        "async_batch_table",
        db=db,
        schema={
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "value": "INTEGER NOT NULL"
        }
    )
    await table.initialize()
    
    # Create batch of records
    records = [
        {"name": f"Item {i}", "value": i * 10}
        for i in range(1, 6)
    ]
    
    # Batch create
    created = await table.batch_create(records)
    assert len(created) == 5
    
    # Store original values
    original_values = {record["id"]: record["value"] for record in created}
    
    # Update records
    for record in created:
        record["value"] = record["value"] + 5
    
    # Batch update
    updated = await table.batch_update(created)
    assert len(updated) == 5
    
    # Verify updates
    for record in updated:
        record_id = record["id"]
        assert record_id in original_values, f"Record with ID {record_id} not found in original records"
        expected_value = original_values[record_id] + 5
        assert record["value"] == expected_value, f"Expected value {expected_value}, got {record['value']}"
    
    print("✅ test_async_batch_operations passed")

async def test_async_transaction(db):
    """Test async transaction."""
    # Create a table
    table = AsyncTable(
        "async_transaction_table",
        db=db,
        schema={
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "balance": "DECIMAL(10,2) NOT NULL"
        }
    )
    await table.initialize()
    
    # Create two accounts
    account1 = await table.create({"name": "Account 1", "balance": Decimal('1000.00')})
    account2 = await table.create({"name": "Account 2", "balance": Decimal('500.00')})
    
    # Define a transaction function
    async def transfer_funds(conn, from_id, to_id, amount):
        # Deduct from source account
        async with conn.cursor() as cur:
            await cur.execute(
                f'UPDATE async_transaction_table SET balance = balance - %s WHERE id = %s',
                (amount, from_id)
            )
            
            # Add to destination account
            await cur.execute(
                f'UPDATE async_transaction_table SET balance = balance + %s WHERE id = %s',
                (amount, to_id)
            )
            
            # Return success message
            return f"Transferred {amount} from {from_id} to {to_id}"
    
    # Execute the transaction
    transfer_amount = Decimal('200.00')
    result = await db.run_in_transaction(
        lambda conn: transfer_funds(conn, account1["id"], account2["id"], transfer_amount)
    )
    
    # Verify the transaction
    updated_account1 = await table.read(account1["id"])
    updated_account2 = await table.read(account2["id"])
    
    # Compare as Decimal
    expected_balance1 = Decimal('800.00')
    expected_balance2 = Decimal('700.00')
    
    assert updated_account1["balance"] == expected_balance1, f"Expected balance {expected_balance1}, got {updated_account1['balance']}"
    assert updated_account2["balance"] == expected_balance2, f"Expected balance {expected_balance2}, got {updated_account2['balance']}"
    
    print("✅ test_async_transaction passed")

async def main():
    """Run the tests."""
    print("Running async tests...")
    
    db = await setup_db()
    migrator, temp_dir = await setup_migrator(db)
    
    try:
        await test_create_migration(migrator, temp_dir)
        await test_load_migrations(migrator, temp_dir)
        await test_async_table_operations(db)
        await test_async_batch_operations(db)
        await test_async_transaction(db)
        # Add more test functions here
        
        print("\nAll tests passed! 🎉")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        await cleanup(db, temp_dir)

if __name__ == "__main__":
    asyncio.run(main()) 