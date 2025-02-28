"""Test async database functionality."""

import os
from decimal import Decimal
import uuid

import pytest
import pytest_asyncio

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
@pytest.mark.asyncio
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


@pytest.mark.asyncio
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


@pytest.mark.asyncio
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


if __name__ == "__main__":
    import pytest
    pytest.main([__file__]) 