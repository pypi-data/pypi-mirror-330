"""Tests for database schema migrations."""

import os
import shutil
from pathlib import Path

import pytest

from manticore_cockroachdb.database import Database
from manticore_cockroachdb.migration import Migration, Migrator


@pytest.fixture
def db():
    """Create database connection."""
    db = Database(
        host="localhost",
        port=26257,
        database="defaultdb",
        user="root",
        password=""
    )
    
    yield db
    
    # Drop all tables
    for table in ["_migrations", "test", "products", "users"]:
        try:
            db.execute(f"DROP TABLE IF EXISTS {table}")
        except:
            pass
    
    db.close()


@pytest.fixture
def migrations_dir(tmp_path):
    """Create temporary migrations directory."""
    path = tmp_path / "migrations"
    path.mkdir()
    yield path
    shutil.rmtree(path)


@pytest.fixture
def migrator(db, migrations_dir):
    """Create migrator instance."""
    return Migrator(db, str(migrations_dir))


def test_create_migration(migrator, migrations_dir):
    """Test creating a new migration."""
    up_sql = "CREATE TABLE test (id INT PRIMARY KEY)"
    down_sql = "DROP TABLE test"
    
    migrator.create_migration("create_test_table", up_sql, down_sql)
    
    # Check migration file was created
    files = list(migrations_dir.glob("*.sql"))
    assert len(files) == 1
    assert files[0].name == "V1__create_test_table.sql"
    
    # Check file contents
    with open(files[0]) as f:
        content = f.read()
        assert content == f"{up_sql}\n\n-- DOWN\n{down_sql}"


def test_load_migrations(migrator, migrations_dir):
    """Test loading migrations from files."""
    # Create some migration files
    migrations = [
        ("create_users", "CREATE TABLE users (id INT PRIMARY KEY)", "DROP TABLE users"),
        ("add_email", "ALTER TABLE users ADD COLUMN email TEXT", "ALTER TABLE users DROP COLUMN email"),
    ]
    
    for i, (desc, up, down) in enumerate(migrations, 1):
        migrator.create_migration(desc, up, down)
    
    # Load migrations
    loaded = migrator.load_migrations()
    assert len(loaded) == 2
    
    assert loaded[0].version == 1
    assert loaded[0].description == "create_users"
    assert loaded[0].up_sql == migrations[0][1]
    assert loaded[0].down_sql == migrations[0][2]
    
    assert loaded[1].version == 2
    assert loaded[1].description == "add_email"
    assert loaded[1].up_sql == migrations[1][1]
    assert loaded[1].down_sql == migrations[1][2]


def test_apply_migrations(migrator, migrations_dir, db):
    """Test applying migrations."""
    # Create migrations
    migrations = [
        (
            "create_products",
            "CREATE TABLE products (id INT PRIMARY KEY, name TEXT)",
            "DROP TABLE products"
        ),
        (
            "add_price",
            "ALTER TABLE products ADD COLUMN price DECIMAL",
            "ALTER TABLE products DROP COLUMN price"
        ),
    ]
    
    for desc, up, down in migrations:
        migrator.create_migration(desc, up, down)
    
    # Apply first migration
    migrator.migrate(target_version=1)
    
    # Check migration was recorded
    versions = migrator.get_applied_versions()
    assert versions == [1]
    
    # Check table was created
    result = db.execute("SHOW TABLES")
    tables = [r["table_name"] for r in result]
    assert "products" in tables
    
    # Apply second migration
    migrator.migrate()
    
    # Check both migrations were applied
    versions = migrator.get_applied_versions()
    assert versions == [1, 2]
    
    # Check column was added
    result = db.execute("SHOW COLUMNS FROM products")
    columns = [r["column_name"] for r in result]
    assert "price" in columns
    
    # Revert to version 1
    migrator.migrate(target_version=1)
    
    # Check second migration was reverted
    versions = migrator.get_applied_versions()
    assert versions == [1]
    
    # Check column was removed
    result = db.execute("SHOW COLUMNS FROM products")
    columns = [r["column_name"] for r in result]
    assert "price" not in columns
    
    # Revert all migrations
    migrator.migrate(target_version=0)
    
    # Check all migrations were reverted
    versions = migrator.get_applied_versions()
    assert versions == []
    
    # Check table was dropped
    result = db.execute("SHOW TABLES")
    tables = [r["table_name"] for r in result]
    assert "products" not in tables


def test_migration_without_down(migrator, migrations_dir):
    """Test migration without down SQL cannot be reverted."""
    # Create migration without down SQL
    migrator.create_migration(
        "test",
        "CREATE TABLE test (id INT PRIMARY KEY)"
    )
    
    # Apply migration
    migrator.migrate()
    
    # Try to revert
    with pytest.raises(ValueError) as exc:
        migrator.migrate(target_version=0)
    assert "cannot be reverted" in str(exc.value)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__]) 