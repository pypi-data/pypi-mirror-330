"""Test async database functionality."""

import os
from decimal import Decimal
import uuid
import pytest
import pytest_asyncio
import asyncio
from psycopg.errors import UndefinedTable, InvalidTableDefinition, DuplicateTable, UniqueViolation

from manticore_cockroachdb.async_database import AsyncDatabase
from .test_utils import requires_async_database


@pytest_asyncio.fixture
async def db():
    """Create test async database."""
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        database = AsyncDatabase.from_url(database_url)
    else:
        database = AsyncDatabase(database="test_db")
    await database.connect()
    yield database
    await database.close()


@requires_async_database
@pytest.mark.anyio
async def test_basic_operations(db):
    """Test basic async database operations."""
    # Create users table
    await db.create_table(
        "async_users",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL",
            "balance": "DECIMAL(19,4) NOT NULL DEFAULT 0.0",
            "active": "BOOLEAN DEFAULT TRUE",
        }
    )

    # Insert a user
    user = await db.insert(
        "async_users",
        {
            "name": "Async Test User",
            "email": "async_test@example.com",
            "balance": Decimal("100.0000"),
        }
    )
    assert user["name"] == "Async Test User"
    assert user["email"] == "async_test@example.com"
    assert user["balance"] == Decimal("100.0000")
    assert user["active"] is True

    # Select the user
    users = await db.select("async_users", where={"email": "async_test@example.com"})
    assert len(users) == 1
    assert users[0]["name"] == "Async Test User"

    # Update the user
    updated = await db.update(
        "async_users",
        {"balance": Decimal("200.0000")},
        {"email": "async_test@example.com"}
    )
    assert updated["balance"] == Decimal("200.0000")

    # Delete the user
    assert await db.delete("async_users", {"email": "async_test@example.com"})

    # Verify deletion
    users = await db.select("async_users", where={"email": "async_test@example.com"})
    assert len(users) == 0

    # Clean up
    await db.drop_table("async_users")


@pytest.mark.anyio
async def test_transaction(db):
    """Test async transaction."""
    # Create test table
    await db.create_table(
        "async_transactions",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "balance": "DECIMAL(19,4) NOT NULL DEFAULT 0.0",
        }
    )

    # Test successful transaction
    async def insert_record(conn):
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO async_transactions (name, balance)
                VALUES (%s, %s)
                RETURNING *
                """,
                ("Alice", Decimal("100.0000"))
            )
            result = await cur.fetchone()
            return result

    result = await db.run_in_transaction(insert_record)
    assert result["name"] == "Alice"
    assert result["balance"] == Decimal("100.0000")

    # Verify record was inserted
    records = await db.select("async_transactions")
    assert len(records) == 1
    assert records[0]["name"] == "Alice"

    # Clean up
    await db.drop_table("async_transactions")


@pytest.mark.anyio
async def test_batch_operations(db):
    """Test async batch operations."""
    # Create test table
    await db.create_table(
        "async_batch_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "value": "INTEGER NOT NULL",
        }
    )

    # Test batch insert
    records = [
        {"name": f"Async Record {i}", "value": i}
        for i in range(5)
    ]
    inserted = await db.batch_insert("async_batch_test", records)
    assert len(inserted) == 5
    for i, record in enumerate(inserted):
        assert record["name"] == f"Async Record {i}"
        assert record["value"] == i

    # Test batch update with subset of columns
    updates = [
        {
            "id": record["id"],
            "value": record["value"] * 2
        }
        for record in inserted
    ]
    updated = await db.batch_update("async_batch_test", updates)
    assert len(updated) == 5
    for i, record in enumerate(updated):
        assert record["name"] == f"Async Record {i}"  # Original name preserved
        assert record["value"] == i * 2  # Updated value

    # Clean up
    await db.drop_table("async_batch_test")


@pytest.mark.anyio
async def test_connection_error_handling():
    """Test handling connection errors with invalid parameters."""
    # Try to connect with invalid host
    db = AsyncDatabase(
        host="nonexistent-host", 
        port=12345
    )
    
    with pytest.raises(Exception):
        await db.connect()


@pytest.mark.anyio
async def test_transaction_rollback(db):
    """Test transaction rollback."""
    # Create a test table
    await db.create_table(
        "transaction_rollback_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "balance": "DECIMAL(10,2) NOT NULL"
        }
    )
    
    # Insert initial data
    alice = await db.insert(
        "transaction_rollback_test",
        {"name": "Alice", "balance": Decimal("100.00")}
    )
    
    # Try a transaction that will fail
    try:
        # Get a transaction object
        tx = await db.transaction()
        # Enter the transaction context
        conn = await tx.__aenter__()
        
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    "UPDATE transaction_rollback_test SET balance = balance - %s WHERE id = %s",
                    (Decimal("50.00"), alice["id"])
                )
                
            # This will cause the transaction to fail
            raise ValueError("Forced error to test rollback")
        except ValueError:
            # Exit the transaction context with the exception
            await tx.__aexit__(ValueError, ValueError("Forced error"), None)
            raise
    except ValueError:
        pass
    
    # Verify the update was rolled back
    result = await db.select("transaction_rollback_test", where={"id": alice["id"]})
    assert result[0]["balance"] == Decimal("100.00")  # Should still be the original value
    
    # Clean up
    await db.drop_table("transaction_rollback_test")


@pytest.mark.anyio
async def test_context_manager_with_errors(db):
    """Test async context manager with errors."""
    # Test that connection is closed even if an error occurs
    test_db = AsyncDatabase(database="test_db")
    await test_db.connect()
    
    try:
        async with test_db:
            # Simulate an error within the context
            raise ValueError("Test error in context")
    except ValueError:
        pass
    
    # Verify connection is closed
    assert test_db._pool is None


@pytest.mark.anyio
async def test_batch_operations_empty_lists(db):
    """Test batch operations with empty lists."""
    # Create test table
    await db.create_table(
        "empty_batch_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL"
        }
    )
    
    # Test batch insert with empty list
    empty_inserted = await db.batch_insert("empty_batch_test", [])
    assert len(empty_inserted) == 0
    
    # Test batch update with empty list
    empty_updated = await db.batch_update("empty_batch_test", [])
    assert len(empty_updated) == 0
    
    # Clean up
    await db.drop_table("empty_batch_test")


@pytest.mark.anyio
async def test_execute_without_fetch(db):
    """Test executing SQL without fetching results."""
    # Create test table
    await db.create_table(
        "execute_no_fetch_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "counter": "INTEGER"
        }
    )
    
    # Execute without fetching results
    result = await db.execute(
        "INSERT INTO execute_no_fetch_test (counter) VALUES (1)",
        fetch=False
    )
    assert result is None
    
    # Verify insertion worked
    records = await db.select("execute_no_fetch_test")
    assert len(records) == 1
    assert records[0]["counter"] == 1
    
    # Clean up
    await db.drop_table("execute_no_fetch_test")


@pytest.mark.anyio
async def test_concurrent_operations(db):
    """Test concurrent operations."""
    # Create test table
    await db.create_table(
        "concurrent_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "counter": "INTEGER NOT NULL DEFAULT 0"
        }
    )
    
    # Insert initial record
    record = await db.insert("concurrent_test", {"counter": 0})
    record_id = record["id"]
    
    # Define concurrent update function with race condition
    async def increment_counter():
        # Get current value
        current = await db.select("concurrent_test", where={"id": record_id})
        current_value = current[0]["counter"]
        
        # Simulate some work
        await asyncio.sleep(0.1)
        
        # Update with incremented value
        await db.update(
            "concurrent_test",
            {"counter": current_value + 1},
            {"id": record_id}
        )
    
    # Run several concurrent updates
    tasks = [increment_counter() for _ in range(5)]
    await asyncio.gather(*tasks)
    
    # Check final value (due to race conditions, might not be 5)
    final = await db.select("concurrent_test", where={"id": record_id})
    
    # The value should be > 0 but might not be 5 due to race conditions
    assert final[0]["counter"] > 0
    
    # Now test with transactions to avoid race conditions
    await db.update("concurrent_test", {"counter": 0}, {"id": record_id})
    
    async def increment_with_transaction():
        async def _increment(conn):
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT counter FROM concurrent_test WHERE id = %s FOR UPDATE",
                    (record_id,)
                )
                current_value = (await cur.fetchone())["counter"]
                
                # Simulate some work
                await asyncio.sleep(0.1)
                
                await cur.execute(
                    "UPDATE concurrent_test SET counter = %s WHERE id = %s",
                    (current_value + 1, record_id)
                )
        
        await db.run_in_transaction(_increment)
    
    # Run several concurrent transactional updates
    tasks = [increment_with_transaction() for _ in range(5)]
    await asyncio.gather(*tasks)
    
    # Check final value (should be exactly 5 with transactions)
    final = await db.select("concurrent_test", where={"id": record_id})
    assert final[0]["counter"] == 5
    
    # Clean up
    await db.drop_table("concurrent_test")


@pytest.mark.anyio
async def test_error_handling_in_execute(db):
    """Test error handling in execute method."""
    # Test with invalid SQL
    with pytest.raises(Exception):
        await db.execute("SELECT * FROM nonexistent_table")
    
    # Test with syntax error
    with pytest.raises(Exception):
        await db.execute("SELECT * FROMM users")


@pytest.mark.anyio
async def test_custom_types(db):
    """Test handling of custom types and JSON data."""
    # Create table with JSONB column
    await db.create_table(
        "json_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "data": "JSONB NOT NULL",
            "tags": "TEXT[]",  # Array type
        }
    )
    
    # Insert with JSON data
    json_data = {
        "name": "Test Item",
        "properties": {
            "color": "red",
            "size": "medium"
        },
        "scores": [1, 2, 3, 4, 5]
    }
    
    tags = ["test", "sample", "json"]
    
    # Import Json for properly handling JSON data
    from psycopg.types.json import Json
    
    record = await db.insert(
        "json_test",
        {"data": Json(json_data), "tags": tags}
    )
    
    # Verify data was stored correctly
    retrieved = await db.select("json_test", where={"id": record["id"]})
    assert retrieved[0]["data"]["name"] == "Test Item"
    assert retrieved[0]["data"]["properties"]["color"] == "red"
    assert retrieved[0]["data"]["scores"][2] == 3
    assert "test" in retrieved[0]["tags"]
    assert len(retrieved[0]["tags"]) == 3
    
    # Query using JSON operators
    result = await db.execute(
        "SELECT * FROM json_test WHERE data->>'name' = %s",
        ("Test Item",)
    )
    assert len(result) == 1
    
    # Clean up
    await db.drop_table("json_test")


@pytest.mark.anyio
async def test_create_drop_database():
    """Test creating and dropping a database."""
    # Connect to default database
    db = AsyncDatabase()
    await db.connect()
    
    # Generate a unique test database name
    test_db_name = f"test_db_{uuid.uuid4().hex[:8]}"
    
    try:
        # Create the database
        await db.create_database(test_db_name)
        
        # Verify it exists
        result = await db.execute("SELECT datname FROM pg_database WHERE datname = %s", (test_db_name,))
        assert len(result) == 1
        assert result[0]["datname"] == test_db_name
        
        # Connect to the new database
        new_db = AsyncDatabase(database=test_db_name)
        await new_db.connect()
        
        # Create a table in the new database
        await new_db.create_table(
            "test_table",
            {"id": "SERIAL PRIMARY KEY", "name": "TEXT"}
        )
        
        # Insert some data
        await new_db.insert("test_table", {"name": "Test"})
        
        # Verify data exists
        result = await new_db.select("test_table")
        assert len(result) == 1
        assert result[0]["name"] == "Test"
        
        # Close connection to the new database
        await new_db.close()
        
    finally:
        # Drop the test database
        await db.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
        await db.close()


@pytest.mark.anyio
async def test_constraint_violation_handling(db):
    """Test handling of constraint violations."""
    # Create table with unique constraint
    await db.create_table(
        "constraint_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "username": "TEXT UNIQUE NOT NULL",
            "email": "TEXT UNIQUE NOT NULL"
        }
    )
    
    # Insert initial record
    await db.insert(
        "constraint_test",
        {"username": "testuser", "email": "test@example.com"}
    )
    
    # Try to insert a record with duplicate username
    with pytest.raises(UniqueViolation):
        await db.insert(
            "constraint_test",
            {"username": "testuser", "email": "another@example.com"}
        )
    
    # Try to insert a record with duplicate email
    with pytest.raises(UniqueViolation):
        await db.insert(
            "constraint_test",
            {"username": "anotheruser", "email": "test@example.com"}
        )
    
    # Verify only one record exists
    count = await db.execute("SELECT COUNT(*) as count FROM constraint_test")
    assert count[0]["count"] == 1
    
    # Clean up
    await db.drop_table("constraint_test")


@pytest.mark.anyio
async def test_multi_statement_transaction(db):
    """Test complex multi-statement transaction."""
    # Create tables for a financial transfer example
    await db.create_table(
        "accounts",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "owner": "TEXT NOT NULL",
            "balance": "DECIMAL(10,2) NOT NULL",
        }
    )
    
    await db.create_table(
        "transactions",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "from_account": "UUID REFERENCES accounts(id)",
            "to_account": "UUID REFERENCES accounts(id)",
            "amount": "DECIMAL(10,2) NOT NULL",
            "timestamp": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        }
    )
    
    # Insert initial accounts
    alice = await db.insert("accounts", {"owner": "Alice", "balance": Decimal("1000.00")})
    bob = await db.insert("accounts", {"owner": "Bob", "balance": Decimal("500.00")})
    
    # Transfer function to run in transaction
    async def transfer_funds(conn, from_id, to_id, amount):
        async with conn.cursor() as cur:
            # Check sufficient funds
            await cur.execute(
                "SELECT balance FROM accounts WHERE id = %s FOR UPDATE",
                (from_id,)
            )
            from_account = await cur.fetchone()
            
            if from_account["balance"] < amount:
                raise ValueError("Insufficient funds")
            
            # Debit from sender
            await cur.execute(
                "UPDATE accounts SET balance = balance - %s WHERE id = %s",
                (amount, from_id)
            )
            
            # Credit to receiver
            await cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE id = %s",
                (amount, to_id)
            )
            
            # Record the transaction
            await cur.execute(
                """
                INSERT INTO transactions 
                (from_account, to_account, amount) 
                VALUES (%s, %s, %s)
                RETURNING *
                """,
                (from_id, to_id, amount)
            )
            transaction = await cur.fetchone()
            
            # Get updated account balances
            await cur.execute(
                "SELECT * FROM accounts WHERE id IN (%s, %s)",
                (from_id, to_id)
            )
            accounts = await cur.fetchall()
            
            return {
                "transaction": transaction,
                "accounts": accounts
            }
    
    # Execute the transfer
    result = await db.run_in_transaction(
        lambda conn: transfer_funds(conn, alice["id"], bob["id"], Decimal("200.00"))
    )
    
    # Check transaction record was created
    assert result["transaction"]["from_account"] == alice["id"]
    assert result["transaction"]["to_account"] == bob["id"]
    assert result["transaction"]["amount"] == Decimal("200.00")
    
    # Check account balances were updated
    updated_accounts = {acct["id"]: acct for acct in result["accounts"]}
    assert updated_accounts[alice["id"]]["balance"] == Decimal("800.00")
    assert updated_accounts[bob["id"]]["balance"] == Decimal("700.00")
    
    # Clean up
    await db.drop_table("transactions")
    await db.drop_table("accounts")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__]) 