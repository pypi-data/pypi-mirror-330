"""Test async migrations."""

import os
import tempfile
import shutil
import uuid
import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from .test_utils import requires_database

from manticore_cockroachdb.async_database import AsyncDatabase
from manticore_cockroachdb.async_migration import AsyncMigrator


@pytest_asyncio.fixture
async def db():
    """Create async test database."""
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        database = AsyncDatabase.from_url(database_url)
    else:
        database = AsyncDatabase(database="test_db")
    
    await database.connect()
    yield database
    await database.close()


@pytest.fixture
def migrations_dir():
    """Create temporary migrations directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest_asyncio.fixture
async def migrator(db, migrations_dir):
    """Create async migrator instance."""
    migrator = AsyncMigrator(db, migrations_dir=migrations_dir)
    await migrator.initialize()
    yield migrator
    try:
        await db.execute("DROP TABLE IF EXISTS _migrations")
    except Exception:
        pass


@pytest.mark.anyio
@requires_database
async def test_create_migration(migrator, migrations_dir):
    """Test creating a migration."""
    # Create a migration
    await migrator.create_migration(
        "create_test_table",
        "CREATE TABLE async_test_table (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_test_table"
    )
    
    # Check that the files were created
    # Find the migration files in the directory
    migration_files = [f for f in os.listdir(migrations_dir) if "create_test_table" in f]
    assert migration_files, "No migration files found for create_test_table"
    
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
        assert "CREATE TABLE async_test_table" in content, "CREATE statement not found in up migration"
    
    with open(down_path, "r") as f:
        content = f.read()
        assert "DROP TABLE async_test_table" in content, "DROP statement not found in down migration"


@pytest.mark.anyio
@requires_database
async def test_load_migrations(migrator, migrations_dir):
    """Test loading migrations."""
    # Create multiple migrations
    await migrator.create_migration(
        "create_users_table",
        "CREATE TABLE async_users (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL)",
        "DROP TABLE async_users"
    )
    
    await migrator.create_migration(
        "add_email_to_users",
        "ALTER TABLE async_users ADD COLUMN email TEXT",
        "ALTER TABLE async_users DROP COLUMN email"
    )
    
    await migrator.create_migration(
        "create_posts_table",
        "CREATE TABLE async_posts (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), title TEXT NOT NULL, content TEXT, user_id UUID REFERENCES async_users(id))",
        "DROP TABLE async_posts"
    )
    
    # Load migrations
    migrations = await migrator.load_migrations()
    
    # Check migrations were loaded
    assert len(migrations) == 3
    
    # Check order is correct
    assert "create_users_table" in migrations[0].name
    assert "add_email_to_users" in migrations[1].name
    assert "create_posts_table" in migrations[2].name


@pytest.mark.anyio
@requires_database
async def test_apply_migrations(migrator, migrations_dir, db):
    """Test applying migrations."""
    # Create multiple migrations
    await migrator.create_migration(
        "create_users_table",
        "CREATE TABLE async_users (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL)",
        "DROP TABLE async_users"
    )
    
    await migrator.create_migration(
        "add_email_to_users",
        "ALTER TABLE async_users ADD COLUMN email TEXT",
        "ALTER TABLE async_users DROP COLUMN email"
    )
    
    # Load migrations
    migrations = await migrator.load_migrations()
    
    # Apply migrations
    await migrator.migrate()
    
    # Get applied versions to check migration status
    applied_versions = await migrator.get_applied_versions()
    assert len(applied_versions) == 2
    assert max(applied_versions) == migrations[1].version
    
    # Check users table exists with email column
    result = await db.execute(
        """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'async_users' AND column_name = 'email'
        """
    )
    assert len(result) == 1
    assert result[0]["column_name"] == "email"
    
    # Apply again - should apply 0 migrations
    await migrator.migrate()
    
    # Should still have the same versions applied
    applied_versions = await migrator.get_applied_versions()
    assert len(applied_versions) == 2
    assert max(applied_versions) == migrations[1].version
    
    # Clean up
    await db.execute("DROP TABLE IF EXISTS async_users")


@pytest.mark.anyio
@requires_database
async def test_migration_without_down(migrator, migrations_dir, db):
    """Test migration that doesn't have a down SQL statement."""
    # Create a migration with no down SQL
    await migrator.create_migration(
        "create_items_table",
        "CREATE TABLE async_items (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL)",
        None  # No down SQL
    )
    
    # Load migrations
    migrations = await migrator.load_migrations()
    
    # Apply migrations
    await migrator.migrate()
    
    # Check items table exists
    result = await db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'async_items'
        """
    )
    assert len(result) == 1
    assert result[0]["table_name"] == "async_items"
    
    # Attempt rollback - should fail
    with pytest.raises(ValueError):
        await migrator.rollback()
    
    # Clean up
    await db.execute("DROP TABLE async_items")


@pytest.mark.anyio
@requires_database
async def test_migration_error_handling(migrator, migrations_dir, db):
    """Test handling of errors in migrations."""
    # Create a valid migration first
    await migrator.create_migration(
        "create_valid_table",
        "CREATE TABLE async_valid_table (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL)",
        "DROP TABLE async_valid_table"
    )
    
    # Create a migration with invalid SQL
    await migrator.create_migration(
        "create_invalid_table",
        "CREATE TABLE async_invalid_table (INVALID SYNTAX",  # Invalid SQL
        "DROP TABLE async_invalid_table"
    )
    
    # Load migrations
    migrations = await migrator.load_migrations()
    
    # Apply migrations - should apply first but fail on second
    with pytest.raises(Exception):
        await migrator.migrate()
    
    # Check valid_table exists
    result = await db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'async_valid_table'
        """
    )
    assert len(result) == 1
    
    # Check migration table shows only the first migration was applied
    result = await db.execute("SELECT * FROM migrations ORDER BY applied_at")
    assert len(result) == 1
    assert "create_valid_table" in result[0]["name"]
    
    # Clean up
    await db.execute("DROP TABLE async_valid_table")


@pytest.mark.anyio
@requires_database
async def test_rollback_error_handling(migrator, migrations_dir, db):
    """Test handling of errors in rollback."""
    # Create a migration with valid up but invalid down SQL
    await migrator.create_migration(
        "create_rollback_test_table",
        "CREATE TABLE async_rollback_test_table (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL)",
        "DROP TABLE nonexistent_table"  # Table name doesn't match
    )
    
    # Load migrations
    migrations = await migrator.load_migrations()
    
    # Apply migrations
    await migrator.migrate()
    
    # Attempt rollback - should fail
    with pytest.raises(Exception):
        await migrator.rollback()
    
    # Table should still exist
    result = await db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'async_rollback_test_table'
        """
    )
    assert len(result) == 1
    
    # Clean up
    await db.execute("DROP TABLE async_rollback_test_table")


@pytest.mark.anyio
@requires_database
async def test_applying_already_applied_migrations(migrator, migrations_dir, db):
    """Test applying migrations that were already applied."""
    # Create migrations
    await migrator.create_migration(
        "create_test_table",
        "CREATE TABLE async_test_table (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL)",
        "DROP TABLE async_test_table"
    )
    
    # Apply migrations
    await migrator.migrate()
    
    # Modify the migration file to change the SQL
    migrations = await migrator.load_migrations()
    migration_file = migrations[0].path
    
    with open(migration_file, "r") as f:
        content = f.read()
    
    modified_content = content.replace(
        "CREATE TABLE async_test_table", 
        "CREATE TABLE async_test_table_modified"
    )
    
    with open(migration_file, "w") as f:
        f.write(modified_content)
    
    # Reload and apply migrations
    await migrator.load_migrations()
    await migrator.migrate()
    
    # Should not apply any migrations since the version is already in the database
    result = await db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'async_test_table'
        """
    )
    assert len(result) == 1
    
    # Clean up
    await db.execute("DROP TABLE async_test_table")


@pytest.mark.anyio
@requires_database
async def test_get_current_version(migrator, migrations_dir, db):
    """Test getting current migration version."""
    # Initially, should have no version
    applied = await migrator.get_applied_versions()
    assert not applied  # No versions applied yet
    
    # Create and apply migrations
    await migrator.create_migration(
        "version_test_1",
        "CREATE TABLE async_version_test_1 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_version_test_1"
    )
    
    await migrator.create_migration(
        "version_test_2",
        "CREATE TABLE async_version_test_2 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_version_test_2"
    )
    
    migrations = await migrator.load_migrations()
    
    # Apply first migration
    await migrator.migrate(target_version=migrations[0].version)
    
    # Check current version
    applied = await migrator.get_applied_versions()
    current_version = max(applied) if applied else None
    assert current_version == migrations[0].version
    
    # Apply second migration
    await migrator.migrate()
    
    # Check current version updated
    applied = await migrator.get_applied_versions()
    current_version = max(applied) if applied else None
    assert current_version == migrations[1].version
    
    # Clean up
    await db.execute("DROP TABLE async_version_test_2")
    await db.execute("DROP TABLE async_version_test_1")


@pytest.mark.anyio
@requires_database
async def test_rollback_to_version(migrator, migrations_dir, db):
    """Test rolling back to a specific version."""
    # Create several migrations
    await migrator.create_migration(
        "rollback_test_1",
        "CREATE TABLE async_rollback_test_1 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_rollback_test_1"
    )
    
    await migrator.create_migration(
        "rollback_test_2",
        "CREATE TABLE async_rollback_test_2 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_rollback_test_2"
    )
    
    await migrator.create_migration(
        "rollback_test_3",
        "CREATE TABLE async_rollback_test_3 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_rollback_test_3"
    )
    
    # Load migrations
    migrations = await migrator.load_migrations()
    
    # Apply all migrations
    await migrator.migrate()
    
    # Verify all tables exist
    for i in range(1, 4):
        result = await db.execute(
            f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'async_rollback_test_{i}'
            """
        )
        assert len(result) == 1
    
    # Rollback to first migration
    target_version = migrations[0].version
    await migrator.migrate(target_version=target_version)
    
    # Check current version using applied versions
    applied_versions = await migrator.get_applied_versions()
    current_version = max(applied_versions) if applied_versions else None
    assert current_version == target_version
    
    # Verify first table exists but others don't
    result = await db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'async_rollback_test_1'
        """
    )
    assert len(result) == 1
    
    for i in range(2, 4):
        result = await db.execute(
            f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'async_rollback_test_{i}'
            """
        )
        assert len(result) == 0
    
    # Clean up
    await db.execute("DROP TABLE async_rollback_test_1")


@pytest.mark.anyio
@requires_database
async def test_get_migration_history(migrator, migrations_dir, db):
    """Test getting migration history."""
    # Create migrations
    await migrator.create_migration(
        "history_test_1",
        "CREATE TABLE async_history_test_1 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_history_test_1"
    )
    
    await migrator.create_migration(
        "history_test_2",
        "CREATE TABLE async_history_test_2 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_history_test_2"
    )
    
    # Load migrations
    migrations = await migrator.load_migrations()
    
    # Apply migrations
    await migrator.migrate()
    
    # Get migration history
    history = await migrator.get_migration_history()
    
    # Check history
    assert len(history) == 2
    assert any("history_test_1" in item["name"] for item in history)
    assert any("history_test_2" in item["name"] for item in history)
    
    # Verify applied_at is set
    for item in history:
        assert item["applied_at"] is not None
    
    # Clean up
    await db.execute("DROP TABLE async_history_test_2")
    await db.execute("DROP TABLE async_history_test_1")


@pytest.mark.anyio
@requires_database
async def test_complex_migration_with_transaction(migrator, migrations_dir, db):
    """Test complex migration with transaction."""
    # Create a migration with multiple statements in a transaction
    sql_up = """
    CREATE TABLE async_categories (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL,
        description TEXT
    );
    
    CREATE TABLE async_products (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        category_id UUID REFERENCES async_categories(id)
    );
    
    -- Insert some initial categories
    INSERT INTO async_categories (name, description) VALUES
    ('Electronics', 'Electronic devices and accessories'),
    ('Books', 'Books and e-books'),
    ('Clothing', 'Apparel and accessories');
    """
    
    sql_down = """
    DROP TABLE async_products;
    DROP TABLE async_categories;
    """
    
    # Create the migration
    await migrator.create_migration("complex_schema", sql_up, sql_down)
    
    # Apply the migration
    await migrator.migrate()
    
    # Verify tables exist
    for table in ["async_categories", "async_products"]:
        result = await db.execute(
            f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = '{table}'
            """
        )
        assert len(result) == 1
    
    # Verify categories were inserted
    result = await db.execute("SELECT COUNT(*) as count FROM async_categories")
    assert result[0]["count"] == 3
    
    # Test the relationship with an insert
    category = (await db.execute("SELECT id FROM async_categories WHERE name = 'Electronics'"))[0]
    
    await db.insert(
        "async_products", 
        {
            "name": "Smartphone", 
            "price": 599.99, 
            "category_id": category["id"]
        }
    )
    
    # Query with join
    result = await db.execute(
        """
        SELECT p.name as product, c.name as category
        FROM async_products p
        JOIN async_categories c ON p.category_id = c.id
        """
    )
    assert len(result) == 1
    assert result[0]["product"] == "Smartphone"
    assert result[0]["category"] == "Electronics"
    
    # Rollback the migration
    await migrator.rollback()
    
    # Verify tables no longer exist
    for table in ["async_categories", "async_products"]:
        result = await db.execute(
            f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = '{table}'
            """
        )
        assert len(result) == 0


@pytest.mark.anyio
@requires_database
async def test_pending_migrations(migrator, migrations_dir, db):
    """Test retrieving pending migrations."""
    # Create migrations
    await migrator.create_migration(
        "pending_test_1",
        "CREATE TABLE async_pending_test_1 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_pending_test_1"
    )
    
    await migrator.create_migration(
        "pending_test_2",
        "CREATE TABLE async_pending_test_2 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_pending_test_2"
    )
    
    await migrator.create_migration(
        "pending_test_3",
        "CREATE TABLE async_pending_test_3 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_pending_test_3"
    )
    
    # Load migrations
    migrations = await migrator.load_migrations()
    
    # Initially all migrations are pending
    applied_versions = await migrator.get_applied_versions()
    pending = [m for m in migrations if m.version not in applied_versions]
    assert len(pending) == 3
    
    # Apply first migration
    await migrator.migrate(target_version=migrations[0].version)
    
    # Now two migrations should be pending
    applied_versions = await migrator.get_applied_versions()
    pending = [m for m in migrations if m.version not in applied_versions]
    assert len(pending) == 2
    assert "pending_test_2" in pending[0].description
    assert "pending_test_3" in pending[1].description
    
    # Apply all migrations
    await migrator.migrate()
    
    # No migrations should be pending
    applied_versions = await migrator.get_applied_versions()
    pending = [m for m in migrations if m.version not in applied_versions]
    assert len(pending) == 0
    
    # Clean up
    for i in range(1, 4):
        await db.execute(f"DROP TABLE async_pending_test_{i}")


@pytest.mark.anyio
@requires_database
async def test_concurrent_migration_operations(migrator, migrations_dir, db):
    """Test concurrent migration operations."""
    # Create migrations
    await migrator.create_migration(
        "concurrent_test_1",
        "CREATE TABLE async_concurrent_test_1 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_concurrent_test_1"
    )
    
    await migrator.create_migration(
        "concurrent_test_2",
        "CREATE TABLE async_concurrent_test_2 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE async_concurrent_test_2"
    )
    
    # Load migrations
    migrations = await migrator.load_migrations()
    
    # Create multiple migrators and apply concurrently
    migrator2 = AsyncMigrator(db, migrations_dir=migrations_dir)
    await migrator2.initialize()
    await migrator2.load_migrations()
    
    # Run in parallel - should not cause conflicts
    results = await asyncio.gather(
        migrator.migrate(),
        migrator2.migrate()
    )
    
    # Verify both tables exist
    for i in range(1, 3):
        result = await db.execute(
            f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'async_concurrent_test_{i}'
            """
        )
        assert len(result) == 1
    
    # Clean up
    for i in range(1, 3):
        await db.execute(f"DROP TABLE async_concurrent_test_{i}")


@pytest.mark.anyio
@requires_database
async def test_apply_migrations_in_batches(migrator, migrations_dir, db):
    """Test applying migrations in batches."""
    # Create a larger set of migrations
    for i in range(1, 6):
        await migrator.create_migration(
            f"batch_test_{i}",
            f"CREATE TABLE async_batch_test_{i} (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
            f"DROP TABLE async_batch_test_{i}"
        )
    
    # Load migrations
    migrations = await migrator.load_migrations()
    
    # Apply first 2 migrations
    await migrator.migrate(target_version=migrations[1].version)
    
    # Apply next 2 migrations
    await migrator.migrate(target_version=migrations[3].version)
    
    # Apply remaining migrations
    await migrator.migrate()
    
    # Verify all 5 tables exist
    for i in range(1, 6):
        result = await db.execute(
            f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'async_batch_test_{i}'
            """
        )
        assert len(result) == 1
    
    # Rollback 2 migrations
    await migrator.migrate(target_version=migrations[2].version)
    
    # Verify only tables 1-3 exist
    for i in range(1, 4):
        result = await db.execute(
            f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'async_batch_test_{i}'
            """
        )
        assert len(result) == 1
    
    for i in range(4, 6):
        result = await db.execute(
            f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'async_batch_test_{i}'
            """
        )
        assert len(result) == 0
    
    # Clean up
    for i in range(1, 4):
        await db.execute(f"DROP TABLE async_batch_test_{i}")


if __name__ == "__main__":
    pytest.main([__file__]) 