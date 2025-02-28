"""Test async CRUD operations."""

import os
from decimal import Decimal
import uuid

import pytest
import pytest_asyncio

from manticore_cockroachdb.async_database import AsyncDatabase
from manticore_cockroachdb.crud.async_table import AsyncTable


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


@pytest_asyncio.fixture
async def users_table(db):
    """Create users table for testing."""
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
    yield table
    await db.drop_table("async_users_table")


@pytest.mark.asyncio
async def test_async_table_create(users_table):
    """Test creating records with async table."""
    # Create a user
    user = await users_table.create({
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    })
    
    assert user["name"] == "John Doe"
    assert user["email"] == "john@example.com"
    assert user["age"] == 30
    assert user["active"] is True
    assert "id" in user


@pytest.mark.asyncio
async def test_async_table_read(users_table):
    """Test reading records with async table."""
    # Create a user
    user = await users_table.create({
        "name": "Jane Smith",
        "email": "jane@example.com",
        "age": 25
    })
    
    # Read the user
    retrieved = await users_table.read(user["id"])
    
    assert retrieved["id"] == user["id"]
    assert retrieved["name"] == "Jane Smith"
    assert retrieved["email"] == "jane@example.com"
    assert retrieved["age"] == 25


@pytest.mark.asyncio
async def test_async_table_update(users_table):
    """Test updating records with async table."""
    # Create a user
    user = await users_table.create({
        "name": "Bob Johnson",
        "email": "bob@example.com",
        "age": 40
    })
    
    # Update the user
    updated = await users_table.update(user["id"], {
        "age": 41,
        "active": False
    })
    
    assert updated["id"] == user["id"]
    assert updated["name"] == "Bob Johnson"  # Unchanged
    assert updated["email"] == "bob@example.com"  # Unchanged
    assert updated["age"] == 41  # Changed
    assert updated["active"] is False  # Changed


@pytest.mark.asyncio
async def test_async_table_delete(users_table):
    """Test deleting records with async table."""
    # Create a user
    user = await users_table.create({
        "name": "Alice Brown",
        "email": "alice@example.com",
        "age": 35
    })
    
    # Delete the user
    result = await users_table.delete(user["id"])
    assert result is True
    
    # Verify deletion
    retrieved = await users_table.read(user["id"])
    assert retrieved is None


@pytest.mark.asyncio
async def test_async_table_list(users_table):
    """Test listing records with async table."""
    # Create multiple users
    users = [
        {"name": "User 1", "email": "user1@example.com", "age": 20},
        {"name": "User 2", "email": "user2@example.com", "age": 25},
        {"name": "User 3", "email": "user3@example.com", "age": 30},
        {"name": "User 4", "email": "user4@example.com", "age": 35},
        {"name": "User 5", "email": "user5@example.com", "age": 40},
    ]
    
    for user in users:
        await users_table.create(user)
    
    # List all users
    all_users = await users_table.list()
    assert len(all_users) >= 5
    
    # List with filter
    young_users = await users_table.list(where={"age": 25})
    assert len(young_users) == 1
    assert young_users[0]["name"] == "User 2"
    
    # List with order
    ordered_users = await users_table.list(order_by="age DESC")
    ordered_ages = [u["age"] for u in ordered_users if u["email"].startswith("user")]
    assert ordered_ages == sorted(ordered_ages, reverse=True)
    
    # List with limit
    limited_users = await users_table.list(limit=2)
    assert len(limited_users) == 2


@pytest.mark.asyncio
async def test_async_table_count(users_table):
    """Test counting records with async table."""
    # Create multiple users
    users = [
        {"name": "Count 1", "email": "count1@example.com", "age": 20, "active": True},
        {"name": "Count 2", "email": "count2@example.com", "age": 25, "active": True},
        {"name": "Count 3", "email": "count3@example.com", "age": 30, "active": False},
    ]
    
    for user in users:
        await users_table.create(user)
    
    # Count all users
    total = await users_table.count()
    assert total >= 3
    
    # Count with filter
    active_count = await users_table.count(where={"active": True})
    assert active_count >= 2
    
    inactive_count = await users_table.count(where={"active": False})
    assert inactive_count >= 1


@pytest.mark.asyncio
async def test_async_table_batch_operations(users_table):
    """Test batch operations with async table."""
    # Create batch of users
    users = [
        {"name": f"Batch User {i}", "email": f"batch{i}@example.com", "age": 20 + i}
        for i in range(1, 6)
    ]
    
    # Batch create
    created = await users_table.batch_create(users)
    assert len(created) == 5
    
    # Store original ages by email
    original_ages = {user["email"]: user["age"] for user in created}
    
    # Update users
    for user in created:
        user["age"] = user["age"] + 1
    
    # Batch update
    updated = await users_table.batch_update(created)
    assert len(updated) == 5
    
    # Verify updates - age should be incremented by 1 for each user
    for user in updated:
        email = user["email"]
        assert email in original_ages, f"User with email {email} not found in original users"
        expected_age = original_ages[email] + 1
        assert user["age"] == expected_age, f"Expected age {expected_age} for {email}, got {user['age']}"


@pytest.mark.asyncio
async def test_async_table_context_manager():
    """Test async table as context manager."""
    db = AsyncDatabase(database="test_db")
    
    async with AsyncTable(
        "async_context_table",
        db=db,
        schema={
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL"
        }
    ) as table:
        # Create a record
        record = await table.create({"name": "Context Test"})
        assert record["name"] == "Context Test"
        
        # Read the record
        retrieved = await table.read(record["id"])
        assert retrieved["name"] == "Context Test"
    
    # Clean up
    await db.drop_table("async_context_table")
    await db.close()


if __name__ == "__main__":
    import pytest
    pytest.main([__file__]) 