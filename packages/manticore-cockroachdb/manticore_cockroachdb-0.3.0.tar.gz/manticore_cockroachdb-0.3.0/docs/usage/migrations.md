# Database Migrations

This guide covers how to use the migration tools to manage database schema changes with the Manticore CockroachDB client.

## Introduction to Migrations

Database migrations are a way to manage changes to your database schema over time. They allow you to:

- Track changes to your database schema
- Apply changes in a consistent way across different environments
- Roll back changes if needed
- Keep a history of all schema changes

The Manticore CockroachDB client provides both synchronous and asynchronous migration tools.

## Synchronous Migrations

### Setting Up Migrations

```python
from manticore_cockroachdb import Database, Migration

# Connect to database
db = Database(database="example_db")

# Create migration instance
migration = Migration(db, migrations_dir="./migrations")
```

### Creating Migrations

```python
# Create a migration to create a users table
migration.create_migration(
    "create users table",  # Description of the migration
    """
    CREATE TABLE users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMPTZ DEFAULT now()
    );
    """,  # Forward SQL (applied during migration)
    """
    DROP TABLE users;
    """  # Undo SQL (applied during rollback)
)

# Create a migration to add a column
migration.create_migration(
    "add age column",
    "ALTER TABLE users ADD COLUMN age INTEGER;",
    "ALTER TABLE users DROP COLUMN age;"
)
```

### Loading Migrations

```python
# Load all migrations from the migrations directory
migrations = migration.load_migrations()

# Print loaded migrations
for m in migrations:
    print(f"Version {m.version}: {m.description}")
```

### Applying Migrations

```python
# Apply all pending migrations
applied_count = migration.migrate()
print(f"Applied {applied_count} migrations")

# Apply migrations up to a specific version
applied_count = migration.migrate(target_version="20230101120000")
print(f"Applied {applied_count} migrations")
```

### Rolling Back Migrations

```python
# Roll back the last migration
rollback_count = migration.rollback()
print(f"Rolled back {rollback_count} migrations")

# Roll back multiple migrations
rollback_count = migration.rollback(count=3)
print(f"Rolled back {rollback_count} migrations")

# Roll back to a specific version
rollback_count = migration.rollback(target_version="20230101120000")
print(f"Rolled back {rollback_count} migrations")
```

### Checking Migration Status

```python
# Get the current migration version
current_version = migration.get_current_version()
print(f"Current version: {current_version}")

# Check if a specific migration has been applied
is_applied = migration.is_applied("20230101120000")
print(f"Migration 20230101120000 applied: {is_applied}")

# Get all applied migrations
applied_migrations = migration.get_applied_migrations()
for m in applied_migrations:
    print(f"Version {m['version']}: {m['description']} (applied at {m['applied_at']})")
```

## Asynchronous Migrations

### Setting Up Migrations

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
        
        # Rest of the migration code...
    finally:
        await db.close()

# Run the async function
asyncio.run(main())
```

### Creating Migrations

```python
# Create a migration to create a users table
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

# Create a migration to add a column
await migration.create_migration(
    "add email verification",
    "ALTER TABLE async_users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;",
    "ALTER TABLE async_users DROP COLUMN email_verified;"
)
```

### Loading Migrations

```python
# Load all migrations from the migrations directory
migrations = await migration.load_migrations()

# Print loaded migrations
for m in migrations:
    print(f"Version {m.version}: {m.description}")
```

### Applying Migrations

```python
# Apply all pending migrations
applied_count = await migration.migrate()
print(f"Applied {applied_count} migrations")

# Apply migrations up to a specific version
applied_count = await migration.migrate(target_version="20230101120000")
print(f"Applied {applied_count} migrations")
```

### Rolling Back Migrations

```python
# Roll back the last migration
rollback_count = await migration.rollback()
print(f"Rolled back {rollback_count} migrations")

# Roll back multiple migrations
rollback_count = await migration.rollback(count=3)
print(f"Rolled back {rollback_count} migrations")

# Roll back to a specific version
rollback_count = await migration.rollback(target_version="20230101120000")
print(f"Rolled back {rollback_count} migrations")
```

### Checking Migration Status

```python
# Get the current migration version
current_version = await migration.get_current_version()
print(f"Current version: {current_version}")

# Check if a specific migration has been applied
is_applied = await migration.is_applied("20230101120000")
print(f"Migration 20230101120000 applied: {is_applied}")

# Get all applied migrations
applied_migrations = await migration.get_applied_migrations()
for m in applied_migrations:
    print(f"Version {m['version']}: {m['description']} (applied at {m['applied_at']})")
```

## Migration File Format

Migration files are stored in the migrations directory with the following naming convention:

```
<version>_<description>.sql
```

For example:

```
20230101120000_create_users_table.sql
20230102130000_add_age_column.sql
```

Each migration file contains both the forward and undo SQL, separated by a special marker:

```sql
-- Forward migration
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- @UNDO

-- Undo migration
DROP TABLE users;
```

## Complete Example

```python
from manticore_cockroachdb import Database, Migration

# Connect to database
db = Database(database="example_db")

try:
    # Create migration instance
    migration = Migration(db, migrations_dir="./migrations")
    
    # Create migrations
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
    
    migration.create_migration(
        "add age column",
        "ALTER TABLE users ADD COLUMN age INTEGER;",
        "ALTER TABLE users DROP COLUMN age;"
    )
    
    # Load migrations
    migrations = migration.load_migrations()
    print(f"Loaded {len(migrations)} migrations")
    
    for m in migrations:
        print(f"Version {m.version}: {m.description}")
    
    # Apply migrations
    applied = migration.migrate()
    print(f"Applied {applied} migrations")
    
    # Insert test data
    db.insert("users", {
        "name": "Migration Test User",
        "email": "migrate@example.com",
        "age": 30
    })
    
    # Show user data
    users = db.select("users")
    print(f"Users in database: {len(users)}")
    
    # Rollback last migration
    rollback_count = migration.rollback(count=1)
    print(f"Rolled back {rollback_count} migrations")
    
    # Apply all migrations again
    applied = migration.migrate()
    print(f"Applied {applied} migrations")
    
finally:
    # Clean up
    db.drop_table("users", if_exists=True)
    db.drop_table("_migrations", if_exists=True)
    
    # Close database connection
    db.close()
``` 