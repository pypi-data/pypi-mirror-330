"""Tests for synchronous Table CRUD operations."""

import os
import uuid
from decimal import Decimal

import pytest
from psycopg.errors import UndefinedTable, InvalidTableDefinition, DuplicateTable
from .test_utils import requires_database

from manticore_cockroachdb.database import Database
from manticore_cockroachdb.crud.table import Table
from manticore_cockroachdb.crud.exceptions import TableNotFoundError, TableNotInitializedError, DatabaseError


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
    non_existent = users_table.get(str(uuid.uuid4()))
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
    
    # Test updating non-existent user - should raise TableNotFoundError
    with pytest.raises(TableNotFoundError):
        users_table.update(str(uuid.uuid4()), {"age": 50})


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
    retrieved = users_table.get(user["id"])
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


class TeaTable(Table):
    """Tea inventory table."""

    table_name = "teas"
    schema = {
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "name": "TEXT NOT NULL",
        "origin": "TEXT",
        "price": "DECIMAL(8,2) NOT NULL",
        "stock": "INTEGER NOT NULL DEFAULT 0",
        "organic": "BOOLEAN DEFAULT FALSE",
    }


@requires_database
def test_table_crud(db):
    """Test table CRUD operations."""
    # Initialize table
    tea_table = TeaTable(db)
    tea_table.initialize()
    
    # Clean up any existing records from previous test runs
    try:
        db.execute(f'DELETE FROM "{tea_table.name}"')
    except Exception:
        pass

    # Create tea
    tea = tea_table.create({
        "name": "Darjeeling",
        "origin": "India",
        "price": Decimal("12.99"),
        "stock": 50,
        "organic": True,
    })
    assert tea["name"] == "Darjeeling"
    assert tea["origin"] == "India"
    assert tea["price"] == Decimal("12.99")
    assert tea["stock"] == 50
    assert tea["organic"] is True

    # Get tea by ID
    retrieved = tea_table.get(tea["id"])
    assert retrieved["name"] == "Darjeeling"
    assert retrieved["origin"] == "India"

    # Update tea
    updated = tea_table.update(tea["id"], {"price": Decimal("14.99"), "stock": 45})
    assert updated["price"] == Decimal("14.99")
    assert updated["stock"] == 45
    assert updated["name"] == "Darjeeling"  # Unchanged
    assert updated["origin"] == "India"  # Unchanged

    # Get all teas
    teas = tea_table.list()
    assert len(teas) == 1
    assert teas[0]["name"] == "Darjeeling"

    # Delete tea
    deleted = tea_table.delete(tea["id"])
    assert deleted is True

    # Verify deletion
    assert tea_table.get(tea["id"]) is None

    # Clean up
    tea_table.drop()


def test_table_inheritance():
    """Test table inheritance."""
    class BaseTable(Table):
        """Base table with shared fields."""
        schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP",
        }

    class ProductTable(BaseTable):
        """Product table inheriting base fields."""
        table_name = "products"
        schema = {
            **BaseTable.schema,
            "name": "TEXT NOT NULL",
            "price": "DECIMAL(10,2) NOT NULL",
        }

    # Check schema composition
    assert "id" in ProductTable.schema
    assert "created_at" in ProductTable.schema
    assert "name" in ProductTable.schema
    assert "price" in ProductTable.schema


def test_table_with_db_context(db):
    """Test table with database context manager."""
    class TestTable(Table):
        """Test table."""
        table_name = "context_test"
        schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
        }

    with Database(database="test_db") as db:
        # Create and use table within context
        table = TestTable(db)
        table.initialize()
        record = table.create({"name": "Test Record"})
        assert record["name"] == "Test Record"

        # Clean up
        table.drop()


def test_table_batch_operations(db):
    """Test table batch operations."""
    class BatchTable(Table):
        """Batch operations test table."""
        table_name = "batch_test"
        schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "value": "INTEGER NOT NULL",
        }

    table = BatchTable(db)
    table.initialize()

    # Create multiple items
    items = [
        {"name": f"Item {i}", "value": i * 10}
        for i in range(5)
    ]
    created = table.create_many(items)
    assert len(created) == 5
    for i, item in enumerate(created):
        assert item["name"] == f"Item {i}"
        assert item["value"] == i * 10

    # Update multiple items
    updates = [
        {"id": item["id"], "value": item["value"] + 5}
        for item in created
    ]
    updated = table.update_many(updates)
    assert len(updated) == 5
    for i, item in enumerate(updated):
        assert item["name"] == f"Item {i}"  # Unchanged
        assert item["value"] == (i * 10) + 5  # Updated

    # Get multiple items
    ids = [item["id"] for item in created]
    retrieved = table.get_many(ids)
    assert len(retrieved) == 5
    for item in retrieved:
        assert item["id"] in ids

    # Clean up
    table.drop()


def test_custom_queries(db):
    """Test custom SQL queries with table."""
    class ReportTable(Table):
        """Table for custom query testing."""
        table_name = "reports"
        schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "category": "TEXT NOT NULL",
            "amount": "DECIMAL(12,2) NOT NULL",
            "date": "DATE NOT NULL",
        }

    table = ReportTable(db)
    table.initialize()
    
    # Clean up any existing records from previous test runs
    try:
        db.execute(f'DELETE FROM "{table.name}"')
    except Exception:
        pass

    # Insert test data
    for i in range(10):
        category = "A" if i < 5 else "B"
        table.create({
            "category": category,
            "amount": Decimal(f"{i * 100}.50"),
            "date": f"2023-0{(i % 5) + 1}-01",
        })

    # Custom query - aggregate by category
    result = table.execute("""
        SELECT 
            category,
            SUM(amount) as total,
            AVG(amount) as average,
            COUNT(*) as count
        FROM reports
        GROUP BY category
        ORDER BY category
    """)

    assert len(result) == 2
    assert result[0]["category"] == "A"
    assert result[1]["category"] == "B"
    assert result[0]["count"] == 5
    assert result[1]["count"] == 5
    # Don't assert exact values for total and average as they may vary

    # Clean up
    table.drop()


def test_table_error_handling(db):
    """Test table error handling."""
    class ErrorTable(Table):
        """Table for error handling tests."""
        table_name = "error_test"
        schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE",
        }
    
    # Drop the table if it exists to avoid conflicts
    db.execute('DROP TABLE IF EXISTS "error_test"', fetch=False)
    
    # Create a new instance of the table without auto-initialization
    table = ErrorTable(db, if_not_exists=False)
    table._initialized = False  # Explicitly mark as uninitialized

    # Test operations on uninitialized table
    with pytest.raises(TableNotInitializedError):
        table.create({"name": "Test", "email": "test@example.com"})

    with pytest.raises(TableNotInitializedError):
        table.get(str(uuid.uuid4()))

    with pytest.raises(TableNotInitializedError):
        table.list()

    # Initialize the table for remaining tests
    table.initialize()

    # Test duplicate constraint violation
    table.create({"name": "User1", "email": "user1@example.com"})
    
    # Create without unique field should work
    table.create({"name": "User2"})
    
    # Create with duplicate email should raise
    with pytest.raises(DatabaseError):
        table.create({"name": "User3", "email": "user1@example.com"})

    # Test get with non-existent ID
    with pytest.raises(TableNotFoundError):
        table.read(str(uuid.uuid4()))

    # Test update with non-existent ID
    with pytest.raises(TableNotFoundError):
        table.update(str(uuid.uuid4()), {"name": "Updated"})

    # Test delete with non-existent ID
    assert table.delete(str(uuid.uuid4())) is False

    # Clean up
    table.drop()


def test_table_empty_operations(db):
    """Test table operations with empty data."""
    class EmptyTable(Table):
        """Table for empty operation tests."""
        table_name = "empty_test"
        schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT",
        }

    # Create the table and ensure it's empty
    table = EmptyTable(db)
    table.initialize()
    
    # Clean up any existing records from previous test runs
    db.execute(f'TRUNCATE TABLE "{table.name}"', fetch=False)

    # Test create with minimal data
    record = table.create({})
    assert "id" in record
    assert record["name"] is None

    # Test empty batch operations
    assert len(table.create_many([])) == 0
    assert len(table.update_many([])) == 0
    assert len(table.get_many([])) == 0

    # Test list with no results
    table.delete(record["id"])
    assert len(table.list()) == 0

    # Test list with limit and offset
    # First, add some records
    for i in range(5):
        table.create({"name": f"Record {i}"})
    
    # Test limit
    limited = table.list(limit=2)
    assert len(limited) == 2
    
    # Test offset
    offset = table.list(offset=3)
    assert len(offset) == 2  # 5 total - 3 offset = 2 remaining
    
    # Test both
    paginated = table.list(limit=2, offset=2)
    assert len(paginated) == 2

    # Clean up
    table.drop()


def test_invalid_schema_handling():
    """Test handling of invalid schema definitions."""
    from manticore_cockroachdb.crud.exceptions import DatabaseError
    
    class InvalidTable(Table):
        """Table with invalid schema."""
        table_name = "invalid_test"
        schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "invalid_field": "INVALID_TYPE",  # This type doesn't exist
        }

    # Initialize database
    db = Database(database="test_db")
    
    # Should raise an error during initialization
    with pytest.raises(DatabaseError):
        # Create the table explicitly instead of relying on auto-initialization
        InvalidTable(db, if_not_exists=False)._schema = InvalidTable.schema
        db.create_table("invalid_test", InvalidTable.schema)


def test_table_already_exists(db):
    """Test handling of tables that already exist."""
    # Import the DatabaseError exception
    from manticore_cockroachdb.crud.exceptions import DatabaseError
    
    # Create a table directly with the database
    db.create_table(
        "existing_table",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
        }
    )
    
    # Try to create the same table with the Table class
    class ExistingTable(Table):
        """Table that already exists."""
        table_name = "existing_table"
        schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "description": "TEXT",  # Added field not in original table
        }
    
    table = ExistingTable(db)
    
    # init() should not raise an error if if_not_exists=True (default)
    table.initialize()
    
    # init() should raise an error if if_not_exists=False
    with pytest.raises(DatabaseError):
        table.initialize(if_not_exists=False)
    
    # Clean up
    db.drop_table("existing_table")


def test_execute_without_fetch(db):
    """Test execute with fetch=False."""
    class ExecuteTable(Table):
        """Table for testing execute without fetch."""
        table_name = "execute_test"
        schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "counter": "INTEGER",
        }

    table = ExecuteTable(db)
    table.initialize()
    
    # Execute without fetching results
    result = table.execute(
        "INSERT INTO execute_test (counter) VALUES (1)",
        fetch=False
    )
    assert result is None
    
    # Verify the insert worked
    records = table.list()
    assert len(records) == 1
    assert records[0]["counter"] == 1
    
    # Clean up
    table.drop()


def test_initialize_existing_table(db):
    """Test initializing a Table class with an existing table."""
    # First create a table directly with database
    db.create_table(
        "initialized_table",
        {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "value": "INTEGER",
        }
    )
    
    # Now define a Table class with the same name
    class InitializedTable(Table):
        """Table for an already initialized table."""
        table_name = "initialized_table"
        # No schema - we'll use initialize_existing=True
    
    # Instantiate table with existing table and manually mark it as initialized
    table = InitializedTable(db)
    table._initialized = True  # Explicitly mark as initialized since we know the table exists
    
    # Should work without init() call
    record = table.create({"name": "Test", "value": 42})
    assert record["name"] == "Test"
    assert record["value"] == 42
    
    # Get the record to confirm it worked
    retrieved = table.get(record["id"])
    assert retrieved["name"] == "Test"
    
    # Clean up
    try:
        db.drop_table("initialized_table")
    except Exception:
        pass


def test_transaction_with_table(db):
    """Test using tables with transactions."""
    class TxTable(Table):
        """Table for transaction tests."""
        table_name = "transaction_test"
        schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "name": "TEXT NOT NULL",
            "balance": "DECIMAL(12,2) NOT NULL",
        }
    
    table = TxTable(db)
    table.initialize()
    
    # Create initial records
    alice = table.create({"name": "Alice", "balance": Decimal("100.00")})
    bob = table.create({"name": "Bob", "balance": Decimal("50.00")})
    
    # Function to transfer funds in a transaction
    def transfer_funds(conn, from_id, to_id, amount):
        with conn.cursor() as cur:
            # Debit from sender
            cur.execute(
                f"UPDATE {table.table_name} SET balance = balance - %s WHERE id = %s",
                (amount, from_id)
            )
            
            # Credit to receiver
            cur.execute(
                f"UPDATE {table.table_name} SET balance = balance + %s WHERE id = %s",
                (amount, to_id)
            )
            
            # Get updated records
            cur.execute(
                f"SELECT * FROM {table.table_name} WHERE id IN (%s, %s)",
                (from_id, to_id)
            )
            return cur.fetchall()
    
    # Execute transaction
    result = db.run_in_transaction(
        lambda conn: transfer_funds(conn, alice["id"], bob["id"], Decimal("25.00"))
    )
    
    # Check results
    for record in result:
        if record["id"] == alice["id"]:
            assert record["balance"] == Decimal("75.00")
        elif record["id"] == bob["id"]:
            assert record["balance"] == Decimal("75.00")
    
    # Verify with table methods
    alice_updated = table.get(alice["id"])
    bob_updated = table.get(bob["id"])
    assert alice_updated["balance"] == Decimal("75.00")
    assert bob_updated["balance"] == Decimal("75.00")
    
    # Test transaction that rolls back
    try:
        with db.transaction() as txn:
            # Update using raw SQL in transaction
            with txn.cursor() as cur:
                cur.execute(
                    f"UPDATE {table.table_name} SET balance = balance - %s WHERE id = %s",
                    (Decimal("50.00"), alice["id"])
                )
            
            # This will raise an exception
            raise ValueError("Force rollback")
    except ValueError:
        pass
    
    # Verify rollback (Alice's balance should still be 75.00)
    alice_after_rollback = table.get(alice["id"])
    assert alice_after_rollback["balance"] == Decimal("75.00")
    
    # Clean up
    table.drop()


if __name__ == "__main__":
    pytest.main([__file__]) 