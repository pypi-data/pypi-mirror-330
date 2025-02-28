"""Tests for synchronous Table CRUD operations."""

import os
import uuid
from decimal import Decimal

import pytest

from manticore_cockroachdb.database import Database
from manticore_cockroachdb.crud.table import Table


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


@pytest.fixture
def users_table(db):
    """Create users table for testing."""
    # Create schema
    schema = {
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "name": "TEXT NOT NULL",
        "email": "TEXT UNIQUE NOT NULL",
        "age": "INTEGER",
        "active": "BOOLEAN DEFAULT TRUE",
    }
    
    # Create Table instance with db and schema
    table = Table("users_table", db=db, schema=schema)
    
    yield table
    
    # Clean up
    db.drop_table("users_table")


def test_table_create(users_table):
    """Test creating records with table."""
    # Create a user
    user = users_table.create({
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    })
    
    assert user["name"] == "John Doe"
    assert user["email"] == "john@example.com"
    assert user["age"] == 30
    assert user["active"] is True
    assert "id" in user


def test_table_read(users_table):
    """Test reading records with table."""
    # Create a user
    user = users_table.create({
        "name": "Jane Smith",
        "email": "jane@example.com",
        "age": 25
    })
    
    # Read the user
    retrieved = users_table.read(user["id"])
    
    assert retrieved["id"] == user["id"]
    assert retrieved["name"] == "Jane Smith"
    assert retrieved["email"] == "jane@example.com"
    assert retrieved["age"] == 25
    
    # Test reading non-existent user
    non_existent = users_table.read(str(uuid.uuid4()))
    assert non_existent is None


def test_table_update(users_table):
    """Test updating records with table."""
    # Create a user
    user = users_table.create({
        "name": "Bob Johnson",
        "email": "bob@example.com",
        "age": 40
    })
    
    # Update the user
    updated = users_table.update(user["id"], {
        "age": 41,
        "active": False
    })
    
    assert updated["id"] == user["id"]
    assert updated["name"] == "Bob Johnson"  # Unchanged
    assert updated["email"] == "bob@example.com"  # Unchanged
    assert updated["age"] == 41  # Changed
    assert updated["active"] is False  # Changed
    
    # Test updating non-existent user
    non_existent = users_table.update(str(uuid.uuid4()), {"age": 50})
    assert non_existent is None


def test_table_delete(users_table):
    """Test deleting records with table."""
    # Create a user
    user = users_table.create({
        "name": "Alice Brown",
        "email": "alice@example.com",
        "age": 35
    })
    
    # Delete the user
    result = users_table.delete(user["id"])
    assert result is True
    
    # Verify deletion
    retrieved = users_table.read(user["id"])
    assert retrieved is None
    
    # Test deleting non-existent user
    result = users_table.delete(str(uuid.uuid4()))
    assert result is False


def test_table_list(users_table):
    """Test listing records with table."""
    # Create multiple users
    users = [
        {"name": "User 1", "email": "user1@example.com", "age": 20},
        {"name": "User 2", "email": "user2@example.com", "age": 25},
        {"name": "User 3", "email": "user3@example.com", "age": 30},
        {"name": "User 4", "email": "user4@example.com", "age": 35},
        {"name": "User 5", "email": "user5@example.com", "age": 40},
    ]
    
    for user in users:
        users_table.create(user)
    
    # List all users
    all_users = users_table.list()
    assert len(all_users) >= 5
    
    # List with filter
    young_users = users_table.list(where={"age": 25})
    assert len(young_users) == 1
    assert young_users[0]["name"] == "User 2"
    
    # List with order
    ordered_users = users_table.list(order_by="age DESC")
    ordered_ages = [u["age"] for u in ordered_users if u["email"].startswith("user")]
    assert ordered_ages == sorted(ordered_ages, reverse=True)
    
    # List with limit
    limited_users = users_table.list(limit=2)
    assert len(limited_users) == 2


def test_table_count(users_table):
    """Test counting records with table."""
    # Create multiple users
    users = [
        {"name": "Count 1", "email": "count1@example.com", "age": 20, "active": True},
        {"name": "Count 2", "email": "count2@example.com", "age": 25, "active": True},
        {"name": "Count 3", "email": "count3@example.com", "age": 30, "active": False},
    ]
    
    for user in users:
        users_table.create(user)
    
    # Count all users
    total = users_table.count(None)
    assert total >= 3
    
    # Count with filter
    active_count = users_table.count(where={"active": True})
    assert active_count >= 2
    
    inactive_count = users_table.count(where={"active": False})
    assert inactive_count >= 1


def test_table_batch_operations(users_table):
    """Test batch operations with table."""
    # Create batch of users
    users = [
        {"name": f"Batch User {i}", "email": f"batch{i}@example.com", "age": 20 + i}
        for i in range(1, 6)
    ]
    
    # Batch create
    created = users_table.batch_create(users)
    assert len(created) == 5
    
    # Store original ages by email
    original_ages = {user["email"]: user["age"] for user in created}
    
    # Update users
    for user in created:
        user["age"] = user["age"] + 1
    
    # Batch update
    updated = users_table.batch_update(created)
    assert len(updated) == 5
    
    # Verify updates - age should be incremented by 1 for each user
    for user in updated:
        email = user["email"]
        assert email in original_ages, f"User with email {email} not found in original users"
        expected_age = original_ages[email] + 1
        assert user["age"] == expected_age, f"Expected age {expected_age} for {email}, got {user['age']}"


def test_table_constructor_with_schema():
    """Test creating a Table with schema in constructor."""
    db = Database(database="test_db")
    
    # Create a new table with schema
    schema = {
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "name": "TEXT NOT NULL",
    }
    
    # Use the constructor with schema
    table = Table(
        "constructor_test",
        db=db,
        schema=schema,
        if_not_exists=True
    )
    
    # Test using the table
    record = table.create({"name": "Constructor Test"})
    assert record["name"] == "Constructor Test"
    
    # Clean up
    db.drop_table("constructor_test")
    db.close()


def test_table_initialize_separately():
    """Test initializing a Table after construction."""
    db = Database(database="test_db")
    
    # Create table without schema
    table = Table("init_test", db=db)
    
    # Initialize schema later
    schema = {
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "name": "TEXT NOT NULL",
    }
    table.initialize(schema)
    
    # Test using the table
    record = table.create({"name": "Initialize Test"})
    assert record["name"] == "Initialize Test"
    
    # Clean up
    db.drop_table("init_test")
    db.close()


def test_table_context_manager():
    """Test using Table as a context manager."""
    db = Database(database="test_db")
    
    # Use table with context manager
    with Table("context_test", db=db, schema={
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "name": "TEXT NOT NULL",
    }) as table:
        # Create a record
        record = table.create({"name": "Context Test"})
        assert record["name"] == "Context Test"
        
        # Read the record
        retrieved = table.read(record["id"])
        assert retrieved["name"] == "Context Test"
    
    # Clean up
    db.drop_table("context_test")
    db.close()


if __name__ == "__main__":
    pytest.main([__file__]) 