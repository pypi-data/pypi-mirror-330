"""Test migrations."""

import os
import tempfile
import shutil
import uuid
from pathlib import Path

import pytest
from .test_utils import requires_database

from manticore_cockroachdb.database import Database
from manticore_cockroachdb.migration import Migrator


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
def migrations_dir():
    """Create temporary migrations directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def migrator(db, migrations_dir):
    """Create migrator instance."""
    migrator = Migrator(db, migrations_dir=migrations_dir)
    yield migrator
    try:
        db.execute("DROP TABLE IF EXISTS migrations")
    except Exception:
        pass


@requires_database
def test_create_migration(migrator, migrations_dir):
    """Test creating a migration."""
    # Create a users table migration
    migration_file = migrator.create_migration(
        "create_users_table",
        "CREATE TABLE users (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL)",
        "DROP TABLE users"
    )
    
    # Check file exists
    assert os.path.exists(migration_file)
    
    # Check file content
    with open(migration_file, "r") as f:
        content = f.read()
        assert "CREATE TABLE users" in content
        assert "DROP TABLE users" in content


@requires_database
def test_load_migrations(migrator, migrations_dir):
    """Test loading migrations."""
    # Create multiple migrations
    migrator.create_migration(
        "create_users_table",
        "CREATE TABLE users (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL)",
        "DROP TABLE users"
    )
    
    migrator.create_migration(
        "add_email_to_users",
        "ALTER TABLE users ADD COLUMN email TEXT",
        "ALTER TABLE users DROP COLUMN email"
    )
    
    migrator.create_migration(
        "create_posts_table",
        "CREATE TABLE posts (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), title TEXT NOT NULL, content TEXT, user_id UUID REFERENCES users(id))",
        "DROP TABLE posts"
    )
    
    # Load migrations
    migrations = migrator.load_migrations()
    
    # Check migrations were loaded
    assert len(migrations) == 3
    
    # Check order is correct
    assert "create_users_table" in migrations[0].name
    assert "add_email_to_users" in migrations[1].name
    assert "create_posts_table" in migrations[2].name


@requires_database
def test_apply_migrations(migrator, migrations_dir, db):
    """Test applying migrations."""
    # Clean up first in case previous test didn't clean up properly
    try:
        db.execute("DROP TABLE IF EXISTS users")
        db.execute("DROP TABLE IF EXISTS _migrations")
        db.execute("DELETE FROM _migrations WHERE description IN ('first', 'add-email')")
    except Exception:
        pass
        
    # Make sure migrations table exists
    migrator._ensure_migrations_table()
    
    # Create migrations
    migrator.create_migration(
        "first",
        "CREATE TABLE users (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL)",
        "DROP TABLE users"
    )
    
    migrator.create_migration(
        "add-email",
        "ALTER TABLE users ADD COLUMN email TEXT",
        "ALTER TABLE users DROP COLUMN email"
    )
    
    # Apply migrations
    result = migrator.migrate()
    assert result.applied > 0
    
    # Verify users table exists
    assert db.exists("users")
    
    # Verify email column exists
    result = db.execute(
        """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'email'
        """
    )
    assert len(result) == 1
    
    # Clean up
    db.execute("DROP TABLE users")
    db.execute("DELETE FROM _migrations WHERE description IN ('first', 'add-email')")


@requires_database
def test_migration_without_down(migrator, migrations_dir, db):
    """Test migrations without down SQL."""
    # Clean up existing tables
    try:
        db.execute("DROP TABLE IF EXISTS no_down_test")
        db.execute("DROP TABLE IF EXISTS _migrations")
        db.execute("DELETE FROM _migrations WHERE description = 'no_down_test'")
    except Exception:
        pass
        
    # Make sure migrations table exists
    migrator._ensure_migrations_table()
        
    # Create migration without down SQL
    migrator.create_migration(
        "no_down_test",
        "CREATE TABLE no_down_test (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        None  # No down SQL
    )
    
    # Apply migration
    result = migrator.migrate()
    assert result.applied > 0
    
    # Verify table exists
    result = db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'no_down_test'
        """
    )
    assert len(result) == 1
    
    # Attempt rollback (should raise ValueError due to missing down SQL)
    applied_versions = migrator.get_applied_versions()
    assert len(applied_versions) > 0
    current_version = max(applied_versions) if applied_versions else 0
    
    # Rolling back to previous version (target_version = current_version - 1)
    # Should raise ValueError about missing down SQL
    with pytest.raises(ValueError, match="cannot be reverted: no down migration provided"):
        migrator.migrate(target_version=current_version - 1)
    
    # Verify table still exists (since rollback failed)
    result = db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'no_down_test'
        """
    )
    assert len(result) == 1
    
    # Clean up
    db.execute("DROP TABLE IF EXISTS no_down_test")
    db.execute("DELETE FROM _migrations WHERE description = 'no_down_test'")


@requires_database
def test_migration_error_handling(migrator, migrations_dir, db):
    """Test handling of errors in migrations."""
    # Clean up first
    try:
        db.execute("DROP TABLE IF EXISTS error_test")
        db.execute("DROP TABLE IF EXISTS _migrations")
        db.execute("DELETE FROM _migrations WHERE description = 'error_test'")
    except Exception:
        pass
        
    # Make sure migrations table exists
    migrator._ensure_migrations_table()
        
    # Create migration with invalid SQL that will definitely fail during execution
    migrator.create_migration(
        "error_test",
        "CREATE TABLE error_test (id NONEXISTENT_TYPE PRIMARY KEY)",  # Invalid SQL that will fail
        "DROP TABLE IF EXISTS error_test"
    )
    
    # Load migrations
    migrations = migrator.load_migrations()
    
    # Attempt to apply migrations (should raise exception due to invalid SQL)
    with pytest.raises(Exception):
        migrator.migrate()
    
    # Verify the table doesn't exist
    result = db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'error_test'
        """
    )
    assert len(result) == 0
    
    # Check no migrations were recorded
    result = db.execute("SELECT * FROM _migrations WHERE description = 'error_test'")
    assert len(result) == 0
    
    # Clean up any potential migration files
    for file in os.listdir(migrations_dir):
        if "error_test" in file:
            os.remove(os.path.join(migrations_dir, file))


@requires_database
def test_rollback_error_handling(migrator, migrations_dir, db):
    """Test error handling during rollback."""
    # Clean up first
    try:
        db.execute("DROP TABLE IF EXISTS rollback_error_test")
        db.execute("DROP TABLE IF EXISTS _migrations")
        db.execute("DELETE FROM _migrations WHERE description = 'rollback_error_test'")
    except Exception:
        pass
        
    # Make sure migrations table exists
    migrator._ensure_migrations_table()
        
    # Create migration with valid up SQL but invalid down SQL
    migrator.create_migration(
        "rollback_error_test",
        "CREATE TABLE rollback_error_test (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "THIS IS NOT VALID SQL"  # Invalid down SQL
    )
    
    # Apply migration
    result = migrator.migrate()
    assert result.applied > 0
    
    # Verify table exists
    result = db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'rollback_error_test'
        """
    )
    assert len(result) == 1
    
    # Get current version
    applied_versions = migrator.get_applied_versions()
    assert len(applied_versions) > 0
    current_version = max(applied_versions) if applied_versions else 0
    
    # Attempt to rollback (should raise exception due to invalid down SQL)
    with pytest.raises(Exception):
        migrator.migrate(target_version=current_version - 1)
    
    # Verify table still exists (rollback failed)
    result = db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'rollback_error_test'
        """
    )
    assert len(result) == 1
    
    # Clean up
    db.execute("DROP TABLE rollback_error_test")
    db.execute("DELETE FROM _migrations WHERE description = 'rollback_error_test'")


@requires_database
def test_applying_already_applied_migrations(migrator, migrations_dir, db):
    """Test that attempting to apply already applied migrations doesn't reapply them."""
    # Clean up first
    try:
        db.execute("DROP TABLE IF EXISTS already_applied_test")
        db.execute("DROP TABLE IF EXISTS _migrations")
        db.execute("DELETE FROM _migrations WHERE description = 'already_applied_test'")
    except Exception:
        pass
        
    # Make sure migrations table exists
    migrator._ensure_migrations_table()
        
    # Create migration
    migrator.create_migration(
        "already_applied_test",
        "CREATE TABLE already_applied_test (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE already_applied_test"
    )
    
    # Apply migration first time
    result1 = migrator.migrate()
    assert result1.applied > 0
    
    # Get count of applied migrations
    applied_count = db.execute("SELECT COUNT(*) FROM _migrations WHERE description = 'already_applied_test'")[0]["count"]
    assert applied_count == 1
    
    # Apply migrations again (should not reapply)
    result2 = migrator.migrate()
    assert result2.applied == 0  # No new migrations applied
    
    # Verify count remains the same
    applied_count = db.execute("SELECT COUNT(*) FROM _migrations WHERE description = 'already_applied_test'")[0]["count"]
    assert applied_count == 1  # Still only one record
    
    # Clean up
    db.execute("DROP TABLE already_applied_test")
    db.execute("DELETE FROM _migrations WHERE description = 'already_applied_test'")


@requires_database
def test_get_current_version(migrator, migrations_dir, db):
    """Test getting current migration version."""
    # Reset migrations table to ensure clean state
    try:
        db.execute("DROP TABLE IF EXISTS _migrations")
        migrator._ensure_migrations_table()
    except Exception:
        pass
        
    # Initially, should have no version
    applied = migrator.get_applied_versions()
    assert len(applied) == 0  # No versions applied yet
    
    # Create and apply a migration
    migrator.create_migration(
        "version_test_1",
        "CREATE TABLE version_test_1 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE version_test_1"
    )
    result = migrator.migrate()
    
    # Should now have version 1
    applied = migrator.get_applied_versions()
    assert len(applied) == 1
    assert applied[0] == 1
    
    # Cleanup
    db.execute("DROP TABLE IF EXISTS version_test_1")
    db.execute("DELETE FROM _migrations WHERE version = 1")


@requires_database
def test_rollback_to_version(migrator, migrations_dir, db):
    """Test rolling back to a specific version."""
    # Reset migrations table to ensure clean state
    try:
        db.execute("DROP TABLE IF EXISTS _migrations")
        migrator._ensure_migrations_table()
        
        # Clean up any existing test tables
        db.execute("DROP TABLE IF EXISTS rollback_test_1")
        db.execute("DROP TABLE IF EXISTS rollback_test_2")
        db.execute("DROP TABLE IF EXISTS rollback_test_3")
    except Exception:
        pass
    
    # Create several migrations
    migrator.create_migration(
        "rollback_test_1",
        "CREATE TABLE rollback_test_1 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE rollback_test_1"
    )
    
    migrator.create_migration(
        "rollback_test_2",
        "CREATE TABLE rollback_test_2 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE rollback_test_2"
    )
    
    migrator.create_migration(
        "rollback_test_3",
        "CREATE TABLE rollback_test_3 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE rollback_test_3"
    )
    
    # Load migrations
    migrations = migrator.load_migrations()
    
    # Apply all migrations
    result = migrator.migrate()
    assert result.applied > 0
    applied = migrator.get_applied_versions()
    assert len(applied) == 3
    
    # Verify all tables exist
    for i in range(1, 4):
        result = db.execute(
            f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name = 'rollback_test_{i}'
            """
        )
        assert len(result) == 1
    
    # Rollback to version 1
    result = migrator.migrate(target_version=1)
    assert result.applied > 0
    
    # Verify tables 2 and 3 no longer exist
    for i in range(2, 4):
        result = db.execute(
            f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name = 'rollback_test_{i}'
            """
        )
        assert len(result) == 0
    
    # Verify table 1 still exists
    result = db.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_name = 'rollback_test_1'
        """
    )
    assert len(result) == 1
    
    # Clean up
    try:
        for i in range(1, 4):
            db.execute(f"DROP TABLE IF EXISTS rollback_test_{i}")
        db.execute("DELETE FROM _migrations WHERE description LIKE 'rollback_test_%'")
    except Exception:
        pass


@requires_database
def test_get_migration_history(migrator, migrations_dir, db):
    """Test getting migration history."""
    # Clean up first in case previous test didn't clean up properly
    try:
        db.execute("DROP TABLE IF EXISTS history_test_1")
        db.execute("DROP TABLE IF EXISTS history_test_2")
        db.execute("DELETE FROM _migrations WHERE description LIKE 'history_test_%'")
    except Exception:
        pass
        
    # Create migrations
    migrator.create_migration(
        "history_test_1",
        "CREATE TABLE history_test_1 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE history_test_1"
    )
    
    migrator.create_migration(
        "history_test_2",
        "CREATE TABLE history_test_2 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE history_test_2"
    )
    
    # Load migrations
    migrations = migrator.load_migrations()
    
    # Apply migrations
    result = migrator.migrate()
    assert result.applied > 0
    
    # Get migration history
    history = migrator.get_migration_history()
    
    # Check history
    assert len(history) == 2
    assert any("history_test_1" in item["description"] for item in history)
    assert any("history_test_2" in item["description"] for item in history)
    
    # Check history contains required fields
    assert "version" in history[0]
    assert "description" in history[0]
    assert "applied_at" in history[0]
    
    # Clean up
    db.execute("DROP TABLE history_test_1")
    db.execute("DROP TABLE history_test_2")
    db.execute("DELETE FROM _migrations WHERE description LIKE 'history_test_%'")


@requires_database
def test_complex_migration_with_transaction(migrator, migrations_dir, db):
    """Test a complex migration with multiple statements in a transaction."""
    # Create a migration with multiple statements (without explicit transaction)
    complex_sql = """
    CREATE TABLE complex_test (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL
    );
    
    CREATE TABLE complex_test_details (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        complex_id UUID NOT NULL REFERENCES complex_test(id),
        details TEXT NOT NULL
    );
    
    INSERT INTO complex_test (id, name) VALUES ('11111111-1111-1111-1111-111111111111', 'Test Record');
    INSERT INTO complex_test_details (id, complex_id, details)
    VALUES ('22222222-2222-2222-2222-222222222222', '11111111-1111-1111-1111-111111111111', 'Test Details');
    """
    
    down_sql = """
    DROP TABLE IF EXISTS complex_test_details;
    DROP TABLE IF EXISTS complex_test;
    """
    
    # Clean up first in case previous test didn't clean up properly
    try:
        db.execute("DROP TABLE IF EXISTS complex_test_details")
        db.execute("DROP TABLE IF EXISTS complex_test")
        db.execute("DROP TABLE IF EXISTS _migrations")
        db.execute("DELETE FROM _migrations WHERE description = 'complex_migration'")
    except Exception:
        pass
    
    # Make sure migrations table exists
    migrator._ensure_migrations_table()
    
    # Create the migration
    migrator.create_migration(
        "complex_migration",
        complex_sql,
        down_sql
    )
    
    # Apply the migration
    result = migrator.migrate()
    assert result.applied > 0
    
    # Verify both tables were created and data was inserted
    result = db.execute("SELECT * FROM complex_test")
    assert len(result) == 1
    assert result[0]["name"] == "Test Record"
    
    details = db.execute("SELECT * FROM complex_test_details")
    assert len(details) == 1
    assert details[0]["details"] == "Test Details"
    
    # Test rollback to previous version
    applied_versions = migrator.get_applied_versions()
    assert len(applied_versions) > 0
    current_version = max(applied_versions) if applied_versions else 0
    result = migrator.migrate(target_version=current_version - 1)
    
    # Verify tables were dropped
    result = db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'complex_test'
        """
    )
    assert len(result) == 0
    
    result = db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'complex_test_details'
        """
    )
    assert len(result) == 0
    
    # Clean up in case the rollback didn't work
    try:
        db.execute("DROP TABLE IF EXISTS complex_test_details")
        db.execute("DROP TABLE IF EXISTS complex_test")
        db.execute("DELETE FROM _migrations WHERE description = 'complex_migration'")
    except Exception:
        pass


@requires_database
def test_pending_migrations(migrator, migrations_dir, db):
    """Test retrieving pending migrations."""
    # Reset migrations table to ensure clean state
    try:
        db.execute("DROP TABLE IF EXISTS _migrations")
        migrator._ensure_migrations_table()
    except Exception:
        pass
        
    # Create migrations
    migrator.create_migration(
        "pending_test_1",
        "CREATE TABLE pending_test_1 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE pending_test_1"
    )
    
    migrator.create_migration(
        "pending_test_2",
        "CREATE TABLE pending_test_2 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE pending_test_2"
    )
    
    migrator.create_migration(
        "pending_test_3",
        "CREATE TABLE pending_test_3 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE pending_test_3"
    )
    
    # Load migrations
    migrations = migrator.load_migrations()
    
    # Initially all migrations are pending
    applied_versions = migrator.get_applied_versions()
    pending = [m for m in migrations if m.version not in applied_versions]
    assert len(pending) == 3
    
    # Apply first migration
    result = migrator.migrate(target_version=migrations[0].version)
    assert result.applied == 1
    
    # Check pending migrations again - should be 2 left
    applied_versions = migrator.get_applied_versions()
    pending = [m for m in migrations if m.version not in applied_versions]
    assert len(pending) == 2
    
    # Clean up
    try:
        db.execute("DROP TABLE IF EXISTS pending_test_1")
        db.execute("DROP TABLE IF EXISTS pending_test_2")
        db.execute("DROP TABLE IF EXISTS pending_test_3")
        db.execute("DELETE FROM _migrations WHERE description LIKE 'pending_test_%'")
    except Exception:
        pass


@requires_database
def test_rollback_method(migrator, migrations_dir, db):
    """Test the rollback method."""
    # Reset migrations table to ensure clean state
    try:
        db.execute("DROP TABLE IF EXISTS _migrations")
        migrator._ensure_migrations_table()
        
        # Clean up any existing test tables
        db.execute("DROP TABLE IF EXISTS rollback_method_test_1")
        db.execute("DROP TABLE IF EXISTS rollback_method_test_2")
        db.execute("DROP TABLE IF EXISTS rollback_method_test_3")
    except Exception:
        pass
    
    # Create several migrations
    migrator.create_migration(
        "rollback_method_test_1",
        "CREATE TABLE rollback_method_test_1 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE rollback_method_test_1"
    )
    
    migrator.create_migration(
        "rollback_method_test_2",
        "CREATE TABLE rollback_method_test_2 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE rollback_method_test_2"
    )
    
    migrator.create_migration(
        "rollback_method_test_3",
        "CREATE TABLE rollback_method_test_3 (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE rollback_method_test_3"
    )
    
    # Apply all migrations
    result = migrator.migrate()
    assert result.applied > 0
    applied = migrator.get_applied_versions()
    assert len(applied) == 3
    
    # Verify all tables exist
    for i in range(1, 4):
        result = db.execute(
            f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name = 'rollback_method_test_{i}'
            """
        )
        assert len(result) == 1
    
    # Test rollback with default count=1 (should rollback just the last migration)
    result = migrator.rollback()
    assert result.applied > 0
    
    # Verify table 3 no longer exists
    result = db.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_name = 'rollback_method_test_3'
        """
    )
    assert len(result) == 0
    
    # Verify tables 1 and 2 still exist
    for i in range(1, 3):
        result = db.execute(
            f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name = 'rollback_method_test_{i}'
            """
        )
        assert len(result) == 1
    
    # Test rollback with count=2 (should rollback the remaining migrations)
    result = migrator.rollback(count=2)
    assert result.applied > 0
    
    # Verify all tables are gone
    for i in range(1, 4):
        result = db.execute(
            f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name = 'rollback_method_test_{i}'
            """
        )
        assert len(result) == 0
    
    # Test rollback when no migrations are applied (should return 0 applied)
    result = migrator.rollback()
    assert result.applied == 0
    
    # Clean up
    try:
        for i in range(1, 4):
            db.execute(f"DROP TABLE IF EXISTS rollback_method_test_{i}")
        db.execute("DELETE FROM _migrations WHERE description LIKE 'rollback_method_test_%'")
    except Exception:
        pass


@requires_database
def test_nonexistent_migrations_dir(db):
    """Test loading migrations from a nonexistent directory."""
    # Create migrator with nonexistent directory
    nonexistent_dir = "/tmp/nonexistent_migrations_dir_" + str(uuid.uuid4())
    migrator = Migrator(db, migrations_dir=nonexistent_dir)
    
    # Load migrations should return empty list
    migrations = migrator.load_migrations()
    assert len(migrations) == 0
    
    # Ensure migrations table was created
    result = db.execute(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = '_migrations'
        """
    )
    assert len(result) == 1
    
    # Clean up
    try:
        db.execute("DROP TABLE IF EXISTS _migrations")
    except Exception:
        pass


@requires_database
def test_invalid_migration_files(migrator, migrations_dir, db):
    """Test handling of invalid migration files."""
    # Create an invalid migration file (not starting with V)
    invalid_file_path = os.path.join(migrations_dir, "invalid_migration.sql")
    with open(invalid_file_path, "w") as f:
        f.write("CREATE TABLE invalid_table (id UUID PRIMARY KEY);")
    
    # Create a file with invalid version format
    invalid_version_path = os.path.join(migrations_dir, "Vx__invalid_version.sql")
    with open(invalid_version_path, "w") as f:
        f.write("CREATE TABLE invalid_version_table (id UUID PRIMARY KEY);")
    
    # Load migrations - should ignore invalid files
    migrations = migrator.load_migrations()
    
    # Verify no migrations were loaded
    assert all(m.name != "invalid_migration" for m in migrations)
    assert all(m.name != "invalid_version" for m in migrations)
    
    # Create a valid migration to verify loading still works
    migrator.create_migration(
        "valid_migration",
        "CREATE TABLE valid_table (id UUID PRIMARY KEY DEFAULT gen_random_uuid())",
        "DROP TABLE valid_table"
    )
    
    # Load migrations again
    migrations = migrator.load_migrations()
    
    # Verify valid migration was loaded
    assert any(m.name == "valid_migration" for m in migrations)
    
    # Clean up
    os.remove(invalid_file_path)
    os.remove(invalid_version_path)
    try:
        db.execute("DROP TABLE IF EXISTS valid_table")
        db.execute("DELETE FROM _migrations WHERE description = 'valid_migration'")
    except Exception:
        pass


if __name__ == "__main__":
    pytest.main([__file__]) 