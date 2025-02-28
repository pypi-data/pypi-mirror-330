"""Test CockroachDB database wrapper."""

import os
from decimal import Decimal
import uuid

import pytest
from .test_utils import requires_database

from manticore_cockroachdb.database import Database


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
        "users",
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
        "users",
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
    users = db.select("users", where={"email": "test@example.com"})
    assert len(users) == 1
    assert users[0]["name"] == "Test User"

    # Update the user
    updated = db.update(
        "users",
        {"balance": Decimal("200.0000")},
        {"email": "test@example.com"}
    )
    assert updated["balance"] == Decimal("200.0000")

    # Delete the user
    assert db.delete("users", {"email": "test@example.com"})

    # Verify deletion
    users = db.select("users", where={"email": "test@example.com"})
    assert len(users) == 0

    # Clean up
    db.drop_table("users")


def test_database_url():
    """Test database creation from URL."""
    url = "postgresql://root@localhost:26257/test_db?sslmode=disable"
    db = Database.from_url(url)
    assert db.database == "test_db"
    assert db.host == "localhost"
    assert db.port == 26257
    assert db.user == "root"
    assert db.sslmode == "disable"
    db.close()


def test_context_manager():
    """Test database context manager."""
    with Database(database="test_db") as db:
        # Create a test table
        db.create_table(
            "test",
            {"id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()"}
        )
        
        # Verify table exists
        result = db.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name = %s",
            ("test",)
        )
        assert len(result) == 1
        
        # Clean up
        db.drop_table("test")


def test_complex_queries(db):
    """Test more complex database operations."""
    # Create accounts table
    db.create_table(
        "accounts",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "owner": "TEXT NOT NULL",
            "balance": "DECIMAL(19,4) NOT NULL DEFAULT 0.0",
            "type": "TEXT NOT NULL",
            "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP",
        }
    )

    # Insert test accounts
    accounts = []
    for i in range(5):
        account = db.insert(
            "accounts",
            {
                "owner": f"User {i}",
                "balance": Decimal(f"{i * 100}.0000"),
                "type": "savings" if i % 2 == 0 else "checking",
            }
        )
        accounts.append(account)

    # Test SELECT with multiple conditions
    savings = db.select(
        "accounts",
        where={"type": "savings"},
        order_by="balance DESC",
        limit=2
    )
    assert len(savings) == 2
    assert savings[0]["balance"] > savings[1]["balance"]

    # Test SELECT specific columns
    balances = db.select(
        "accounts",
        columns=["owner", "balance"],
        where={"type": "checking"},
        order_by="balance DESC"
    )
    assert len(balances) == 2
    assert "type" not in balances[0]
    assert "created_at" not in balances[0]

    # Clean up
    db.drop_table("accounts")


def test_transactions(db):
    """Test transaction operations."""
    # Create test table
    db.create_table(
        "transactions",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "balance": "DECIMAL(19,4) NOT NULL DEFAULT 0.0",
        }
    )

    # Test successful transaction
    with db.transaction() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO transactions (name, balance)
                VALUES (%s, %s)
                RETURNING *
                """,
                ("Alice", Decimal("100.0000"))
            )
            result = cur.fetchone()
            assert result["name"] == "Alice"
            assert result["balance"] == Decimal("100.0000")

    # Test transaction rollback
    try:
        with db.transaction() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO transactions (name, balance)
                    VALUES (%s, %s)
                    RETURNING *
                    """,
                    ("Bob", Decimal("200.0000"))
                )
                result = cur.fetchone()
                assert result["name"] == "Bob"
                # Raise exception to trigger rollback
                raise ValueError("Test rollback")
    except ValueError:
        pass

    # Verify only Alice's record exists
    results = db.select("transactions")
    assert len(results) == 1
    assert results[0]["name"] == "Alice"

    # Test run_in_transaction
    def transfer(conn):
        with conn.cursor() as cur:
            # Insert Charlie
            cur.execute(
                """
                INSERT INTO transactions (name, balance)
                VALUES (%s, %s)
                RETURNING *
                """,
                ("Charlie", Decimal("300.0000"))
            )
            charlie = cur.fetchone()

            # Update Alice's balance
            cur.execute(
                """
                UPDATE transactions
                SET balance = balance + %s
                WHERE name = %s
                RETURNING *
                """,
                (Decimal("50.0000"), "Alice")
            )
            alice = cur.fetchone()

            return [charlie, alice]

    results = db.run_in_transaction(transfer)
    assert len(results) == 2
    assert results[0]["name"] == "Charlie"
    assert results[0]["balance"] == Decimal("300.0000")
    assert results[1]["name"] == "Alice"
    assert results[1]["balance"] == Decimal("150.0000")

    # Clean up
    db.drop_table("transactions")


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
        {"name": f"Record {i}", "value": i}
        for i in range(5)
    ]
    inserted = db.batch_insert("batch_test", records)
    assert len(inserted) == 5
    for i, record in enumerate(inserted):
        assert record["name"] == f"Record {i}"
        assert record["value"] == i

    # Test batch update with subset of columns
    updates = [
        {
            "id": record["id"],
            "value": record["value"] * 2
        }
        for record in inserted
    ]
    updated = db.batch_update("batch_test", updates)
    assert len(updated) == 5
    for i, record in enumerate(updated):
        assert record["name"] == f"Record {i}"  # Original name preserved
        assert record["value"] == i * 2  # Updated value

    # Test batch update with invalid data
    with pytest.raises(ValueError):
        db.batch_update("batch_test", [{"id": record["id"]} for record in updated])

    # Clean up
    db.drop_table("batch_test")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__]) 