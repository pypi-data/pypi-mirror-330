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

::: manticore_cockroachdb.async_migration.AsyncMigration
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
from manticore_cockroachdb import AsyncDatabase, AsyncMigration

async def main():
    # Connect to database
    db = AsyncDatabase(database="example_db")
    await db.connect()
    
    try:
        # Create migration instance
        migration = AsyncMigration(db, migrations_dir="./async_migrations")
        
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
        applied = await migration.migrate()
        print(f"Applied {applied} migrations")
        
        # Rollback last migration
        rollback_count = await migration.rollback(count=1)
        print(f"Rolled back {rollback_count} migrations")
        
    finally:
        await db.close()

# Run the async function
asyncio.run(main())
``` 