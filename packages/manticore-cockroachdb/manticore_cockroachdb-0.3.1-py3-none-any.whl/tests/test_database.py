"""Test CockroachDB database wrapper."""

import os
from decimal import Decimal
import uuid

import pytest
from .test_utils import requires_database

from manticore_cockroachdb.database import Database
from manticore_cockroachdb.crud.exceptions import DatabaseError


@pytest.fixture
def db():
    """Create test database."""
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        database = Database.from_url(database_url)
    else:
        database = Database(database="test_db")
    yield database
    database.close()


@requires_database
def test_basic_operations(db):
    """Test basic database operations."""
    # Create users table
    db.create_table(
        "test_users",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL",
            "balance": "DECIMAL(19,4) NOT NULL DEFAULT 0.0",
            "active": "BOOLEAN DEFAULT TRUE",
        }
    )

    # Insert a user
    user = db.insert(
        "test_users",
        {
            "name": "Test User",
            "email": "test@example.com",
            "balance": Decimal("100.0000"),
        }
    )
    assert user["name"] == "Test User"
    assert user["email"] == "test@example.com"
    assert user["balance"] == Decimal("100.0000")
    assert user["active"] is True

    # Select the user
    users = db.select("test_users", where={"email": "test@example.com"})
    assert len(users) == 1
    assert users[0]["name"] == "Test User"

    # Update the user
    updated = db.update(
        "test_users",
        {"balance": Decimal("200.0000")},
        {"email": "test@example.com"}
    )
    assert updated["balance"] == Decimal("200.0000")

    # Delete the user
    assert db.delete("test_users", {"email": "test@example.com"})

    # Verify deletion
    users = db.select("test_users", where={"email": "test@example.com"})
    assert len(users) == 0

    # Clean up
    db.drop_table("test_users")


def test_database_url():
    """Test database URL parsing."""
    db = Database.from_url("postgresql://user:pass@localhost:5432/testdb?sslmode=require", connect=False)
    assert db.host == "localhost"
    assert db.port == 5432
    assert db.database == "testdb"
    assert db.user == "user"
    assert db.password == "pass"
    assert db.sslmode == "require"


def test_context_manager():
    """Test database as context manager."""
    with Database(database="test_db") as db:
        # Check connection is open
        assert db._pool is not None
        # Execute a query
        result = db.execute("SELECT 1 AS value")
        assert result[0]["value"] == 1
    
    # Connection should be closed
    assert db._pool is None


def test_complex_queries(db):
    """Test more complex SQL queries."""
    # Create a test table
    db.create_table(
        "complex_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "category": "TEXT NOT NULL",
            "value": "INTEGER NOT NULL",
            "timestamp": "TIMESTAMPTZ DEFAULT now()",
        }
    )
    
    # Insert test data
    categories = ["A", "B", "C"]
    for i in range(10):
        db.insert(
            "complex_test",
            {
                "name": f"Item {i}",
                "category": categories[i % 3],
                "value": i * 10,
            }
        )
    
    # Test aggregate query
    result = db.execute("""
        SELECT 
            category, 
            COUNT(*) as count, 
            SUM(value) as total, 
            AVG(value) as average
        FROM complex_test
        GROUP BY category
        ORDER BY category
    """)
    
    assert len(result) == 3
    for row in result:
        assert row["category"] in categories
        assert row["count"] > 0
        assert row["total"] >= 0
    
    # Test filtering with subquery
    result = db.execute("""
        SELECT name, value
        FROM complex_test
        WHERE value > (SELECT AVG(value) FROM complex_test)
        ORDER BY value DESC
    """)
    
    # Should have the higher values
    assert len(result) > 0
    for i in range(1, len(result)):
        assert result[i-1]["value"] >= result[i]["value"]
    
    # Clean up
    db.drop_table("complex_test")


def test_transactions(db):
    """Test transaction handling."""
    # Create test table
    db.create_table(
        "transaction_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "balance": "DECIMAL(19,4) NOT NULL"
        }
    )
    
    # First, insert some test data
    user1 = db.insert("transaction_test", {"name": "Alice", "balance": Decimal("1000.0000")})
    user2 = db.insert("transaction_test", {"name": "Bob", "balance": Decimal("500.0000")})
    
    # Test successful transaction with context manager
    with db.transaction() as txn:
        # Update Alice's balance
        with txn.cursor() as cur:
            cur.execute(
                "UPDATE transaction_test SET balance = balance - %s WHERE id = %s",
                (Decimal("100.0000"), user1["id"])
            )
            
        # Update Bob's balance
        with txn.cursor() as cur:
            cur.execute(
                "UPDATE transaction_test SET balance = balance + %s WHERE id = %s",
                (Decimal("100.0000"), user2["id"])
            )
    
    # Verify changes were committed
    alice = db.select("transaction_test", where={"id": user1["id"]})[0]
    bob = db.select("transaction_test", where={"id": user2["id"]})[0]
    
    assert alice["balance"] == Decimal("900.0000")
    assert bob["balance"] == Decimal("600.0000")
    
    # Test rollback on exception
    try:
        with db.transaction() as txn:
            # Update Alice's balance
            with txn.cursor() as cur:
                cur.execute(
                    "UPDATE transaction_test SET balance = balance - %s WHERE id = %s",
                    (Decimal("200.0000"), user1["id"])
                )
                
            # Try to update nonexistent user (should fail)
            with txn.cursor() as cur:
                # Use a WHERE clause that won't match any rows instead of a non-existent ID
                # This won't raise an exception but will still not update any rows
                cur.execute(
                    "UPDATE transaction_test SET balance = balance + %s WHERE id = %s AND name = 'NonExistentName'",
                    (Decimal("200.0000"), user2["id"])
                )
                
            # Explicitly raise an exception to trigger rollback
            raise ValueError("Forcing transaction rollback")
                
    except ValueError:
        pass  # Expected to fail
    
    # Verify transaction was rolled back
    alice = db.select("transaction_test", where={"id": user1["id"]})[0]
    assert alice["balance"] == Decimal("900.0000")  # Still the same
    
    # Test transaction using run_in_transaction
    def transfer(conn):
        """Transfer funds between accounts."""
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE transaction_test SET balance = balance - %s WHERE id = %s",
                (Decimal("50.0000"), user1["id"])
            )
            
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE transaction_test SET balance = balance + %s WHERE id = %s",
                (Decimal("50.0000"), user2["id"])
            )
            
        with conn.cursor() as cur:
            cur.execute(
                "SELECT name, balance FROM transaction_test WHERE id IN (%s, %s)",
                (user1["id"], user2["id"])
            )
            return cur.fetchall()
    
    # Run the transfer in a transaction
    result = db.run_in_transaction(transfer)
    
    # Check the returned data
    for row in result:
        if row["name"] == "Alice":
            assert row["balance"] == Decimal("850.0000")
        elif row["name"] == "Bob":
            assert row["balance"] == Decimal("650.0000")
    
    # Clean up
    db.drop_table("transaction_test")


def test_batch_operations(db):
    """Test batch operations."""
    # Create test table
    db.create_table(
        "batch_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "value": "INTEGER NOT NULL",
        }
    )
    
    # Test batch insert
    records = [
        {"name": f"Batch Record {i}", "value": i}
        for i in range(5)
    ]
    inserted = db.batch_insert("batch_test", records)
    assert len(inserted) == 5
    for i, record in enumerate(inserted):
        assert record["name"] == f"Batch Record {i}"
        assert record["value"] == i
    
    # Test batch update with subset of columns
    updates = [
        {
            "id": record["id"],
            "value": record["value"] * 10
        }
        for record in inserted
    ]
    updated = db.batch_update("batch_test", updates)
    assert len(updated) == 5
    for i, record in enumerate(updated):
        assert record["name"] == f"Batch Record {i}"  # Original name preserved
        assert record["value"] == i * 10  # Updated value
    
    # Clean up
    db.drop_table("batch_test")


def test_connection_error_handling():
    """Test handling of connection errors."""
    # Import the ConnectionError exception
    from manticore_cockroachdb.crud.exceptions import ConnectionError
    
    # Invalid connection parameters should raise ConnectionError
    with pytest.raises(ConnectionError):
        # This should raise a ConnectionError during initialization
        Database(host="nonexistent-host", port=12345, connect_timeout=1)


def test_transaction_manual_commit_rollback():
    """Test manual commit and rollback of transactions."""
    # Set up database
    db = Database(database="test_db")
    
    # Create test table
    db.create_table(
        "manual_tx_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "counter": "INTEGER NOT NULL",
        }
    )
    
    # Insert initial record
    db.insert("manual_tx_test", {"counter": 0})
    
    # Test manual commit
    tx = db.transaction()
    try:
        # Use the connection from the transaction to create a cursor
        with tx as conn:
            # Create a cursor from the connection
            with conn.cursor() as cur:
                cur.execute("UPDATE manual_tx_test SET counter = counter + 1")
        
        # Commit the transaction
        tx.commit()
        
        # Check counter was incremented
        result = db.select("manual_tx_test")[0]
        assert result["counter"] == 1
        
        # Test manual rollback
        tx = db.transaction()
        with tx as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE manual_tx_test SET counter = counter + 1")
            
            # Don't commit - rollback instead
            tx.rollback()
        
        # Check counter didn't change
        result = db.select("manual_tx_test")[0]
        assert result["counter"] == 1
    finally:
        # Clean up
        db.drop_table("manual_tx_test")
        db.close()


def test_batch_operations_empty_lists(db):
    """Test batch operations with empty lists."""
    # Create test table
    db.create_table(
        "empty_batch_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
        }
    )
    
    # Test batch insert with empty list
    empty_inserted = db.batch_insert("empty_batch_test", [])
    assert len(empty_inserted) == 0
    
    # Test batch update with empty list
    empty_updated = db.batch_update("empty_batch_test", [])
    assert len(empty_updated) == 0
    
    # Clean up
    db.drop_table("empty_batch_test")


def test_execute_without_fetch(db):
    """Test execute with fetch=False."""
    # Create test table
    db.create_table(
        "no_fetch_test",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "counter": "INTEGER",
        }
    )
    
    # Execute without fetching results
    result = db.execute(
        "INSERT INTO no_fetch_test (counter) VALUES (1)",
        fetch=False
    )
    assert result is None
    
    # Verify the insert worked
    records = db.select("no_fetch_test")
    assert len(records) == 1
    assert records[0]["counter"] == 1
    
    # Clean up
    db.drop_table("no_fetch_test")


def test_create_database():
    """Test creating a database."""
    db = Database()
    test_db_name = f"test_db_{uuid.uuid4().hex[:8]}"
    
    try:
        # Create the database
        db.create_database(test_db_name)
        
        # Verify it exists
        result = db.execute("SELECT datname FROM pg_database WHERE datname = %s", (test_db_name,))
        assert len(result) == 1
        assert result[0]["datname"] == test_db_name
        
    finally:
        # Clean up (drop the database)
        db.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
        db.close()


if __name__ == "__main__":
    pytest.main([__file__]) 