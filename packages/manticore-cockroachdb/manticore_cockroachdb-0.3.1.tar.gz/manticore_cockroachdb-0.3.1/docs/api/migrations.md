# Migrations API

The Manticore CockroachDB client provides both synchronous and asynchronous migration support to help manage database schema changes.

## Synchronous Migration

::: manticore_cockroachdb.migration.Migration
    options:
      show_root_heading: true
      show_root_full_path: false
      show_source: true
      heading_level: 3
      members_order: source

## Asynchronous Migration

> **Note:** The AsyncMigrator class supports two methods for reverting migrations:
> 1. Using the `migrate()` method with a `target_version` parameter to revert to a specific version
> 2. Manually executing the down SQL and removing migration records for more fine-grained control

::: manticore_cockroachdb.async_migration.AsyncMigrator
    options:
      show_root_heading: true
      show_root_full_path: false
      show_source: true
      heading_level: 3
      members_order: source

## Usage Examples

### Synchronous Migrations

```python
from manticore_cockroachdb import Database, Migration

# Connect to database
db = Database(database="example_db")

# Create migration instance
migration = Migration(db, migrations_dir="./migrations")

# Create a new migration
migration.create_migration(
    "create users table",
    """
    CREATE TABLE users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMPTZ DEFAULT now()
    );
    """,
    """
    DROP TABLE users;
    """
)

# Load migrations
migrations = migration.load_migrations()
print(f"Loaded {len(migrations)} migrations")

# Apply migrations
applied = migration.migrate()
print(f"Applied {applied} migrations")

# Rollback last migration
rollback_count = migration.rollback(count=1)
print(f"Rolled back {rollback_count} migrations")
```

### Asynchronous Migrations

```python
import asyncio
from manticore_cockroachdb.async_database import AsyncDatabase
from manticore_cockroachdb.async_migration import AsyncMigrator

async def main():
    # Connect to database
    db = AsyncDatabase(database="example_db")
    await db.connect()
    
    try:
        # Create migration instance
        migration = AsyncMigrator(db, migrations_dir="./async_migrations")
        
        # Initialize the migrator (creates the _migrations table)
        await migration.initialize()
        
        # Create a new migration
        await migration.create_migration(
            "create async users table",
            """
            CREATE TABLE async_users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMPTZ DEFAULT now()
            );
            """,
            """
            DROP TABLE async_users;
            """
        )
        
        # Load migrations
        migrations = await migration.load_migrations()
        print(f"Loaded {len(migrations)} migrations")
        
        # Apply migrations
        await migration.migrate()
        print("Migrations applied successfully")
        
        # Method 1: Revert using migrate with target_version
        # This will revert to version 0 (before any migrations)
        await migration.migrate(target_version=0)
        print("Reverted all migrations using migrate method")
        
        # Method 2: Manual migration reversion
        # This approach gives you more control over the reversion process
        last_migration = max(migrations, key=lambda m: m.version)
        
        # Execute the down SQL directly
        if last_migration.down_sql:
            await db.execute(last_migration.down_sql)
            await db.execute(
                "DELETE FROM _migrations WHERE version = %s",
                (last_migration.version,)
            )
            print(f"Manually reverted migration V{last_migration.version}")
        
    finally:
        await db.close()

# Run the async function
asyncio.run(main()) 