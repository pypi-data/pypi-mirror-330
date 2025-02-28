"""Tests for async database schema migrations."""

import os
import shutil
from pathlib import Path

import pytest
import pytest_asyncio

from manticore_cockroachdb.async_database import AsyncDatabase
from manticore_cockroachdb.async_migration import AsyncMigration, AsyncMigrator


@pytest_asyncio.fixture
async def db():
    """Create async database connection."""
    db = AsyncDatabase(
        host="localhost",
        port=26257,
        database="defaultdb",
        user="root",
        password=""
    )
    await db.connect()
    
    yield db
    
    # Drop all tables
    for table in ["_migrations", "async_test", "async_products", "async_users"]:
        try:
            await db.execute(f"DROP TABLE IF EXISTS {table}")
        except:
            pass
    
    await db.close()


@pytest_asyncio.fixture
async def migrations_dir(tmp_path):
    """Create temporary migrations directory."""
    path = tmp_path / "async_migrations"
    path.mkdir()
    yield path
    shutil.rmtree(path)


@pytest_asyncio.fixture
async def migrator(db, migrations_dir):
    """Create async migrator instance."""
    migrator = AsyncMigrator(db, str(migrations_dir))
    await migrator.initialize()
    return migrator


@pytest.mark.asyncio
async def test_create_migration(migrator, migrations_dir):
    """Test creating a new async migration."""
    up_sql = "CREATE TABLE async_test (id INT PRIMARY KEY)"
    down_sql = "DROP TABLE async_test"
    
    await migrator.create_migration("create_async_test_table", up_sql, down_sql)
    
    # Check migration files were created
    files = list(migrations_dir.glob("*.sql"))
    assert len(files) == 2
    
    # Check forward migration file
    forward_file = migrations_dir / "V1__create_async_test_table.sql"
    assert forward_file.exists()
    
    # Check undo migration file
    undo_file = migrations_dir / "U1__undo_create_async_test_table.sql"
    assert undo_file.exists()
    
    # Check file contents
    with open(forward_file) as f:
        content = f.read()
        assert content == up_sql
        
    # Check undo file contents
    with open(undo_file) as f:
        content = f.read()
        assert content == down_sql


@pytest.mark.asyncio
async def test_load_migrations(migrator, migrations_dir):
    """Test loading async migrations from files."""
    # Create some migration files
    migrations = [
        ("create_async_users", "CREATE TABLE async_users (id INT PRIMARY KEY)", "DROP TABLE async_users"),
        ("add_email", "ALTER TABLE async_users ADD COLUMN email TEXT", "ALTER TABLE async_users DROP COLUMN email"),
    ]
    
    for i, (desc, up, down) in enumerate(migrations, 1):
        await migrator.create_migration(desc, up, down)
    
    # Load migrations
    loaded = await migrator.load_migrations()
    assert len(loaded) == 2
    
    assert loaded[0].version == 1
    assert loaded[0].description == "create async users"
    assert loaded[0].up_sql == migrations[0][1]
    assert loaded[0].down_sql == migrations[0][2]
    
    assert loaded[1].version == 2
    assert loaded[1].description == "add email"
    assert loaded[1].up_sql == migrations[1][1]
    assert loaded[1].down_sql == migrations[1][2]


@pytest.mark.asyncio
async def test_apply_migrations(migrator, migrations_dir, db):
    """Test applying async migrations."""
    # Create migrations
    migrations = [
        (
            "create_async_products",
            "CREATE TABLE async_products (id INT PRIMARY KEY, name TEXT)",
            "DROP TABLE async_products"
        ),
        (
            "add_price",
            "ALTER TABLE async_products ADD COLUMN price DECIMAL",
            "ALTER TABLE async_products DROP COLUMN price"
        ),
    ]
    
    for desc, up, down in migrations:
        await migrator.create_migration(desc, up, down)
    
    # Apply first migration
    await migrator.migrate(target_version=1)
    
    # Check migration was recorded
    versions = await migrator.get_applied_versions()
    assert versions == [1]
    
    # Check table was created
    result = await db.execute("SHOW TABLES")
    tables = [r["table_name"] for r in result]
    assert "async_products" in tables
    
    # Apply second migration
    await migrator.migrate()
    
    # Check both migrations were applied
    versions = await migrator.get_applied_versions()
    assert versions == [1, 2]
    
    # Check column was added
    result = await db.execute("SHOW COLUMNS FROM async_products")
    columns = [r["column_name"] for r in result]
    assert "price" in columns
    
    # Revert to version 1
    await migrator.migrate(target_version=1)
    
    # Check second migration was reverted
    versions = await migrator.get_applied_versions()
    assert versions == [1]
    
    # Check column was removed
    result = await db.execute("SHOW COLUMNS FROM async_products")
    columns = [r["column_name"] for r in result]
    assert "price" not in columns
    
    # Revert all migrations
    await migrator.migrate(target_version=0)
    
    # Check all migrations were reverted
    versions = await migrator.get_applied_versions()
    assert versions == []
    
    # Check table was dropped
    result = await db.execute("SHOW TABLES")
    tables = [r["table_name"] for r in result]
    assert "async_products" not in tables

if __name__ == "__main__":
    import pytest
    pytest.main([__file__]) 