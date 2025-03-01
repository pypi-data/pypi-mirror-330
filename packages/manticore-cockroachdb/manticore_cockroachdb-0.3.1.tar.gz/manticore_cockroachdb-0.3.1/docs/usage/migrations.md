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
await migration.migrate()
print("Migrations applied successfully")

# Apply migrations up to a specific version
await migration.migrate(target_version=2)
print("Migrations applied successfully up to version 2")
```

### Manual Migration Reversion

The `AsyncMigrator` class doesn't have a built-in rollback method, but you can manually revert migrations:

```python
# Load migrations
migrations = await migration.load_migrations()

# Get the last migration
last_migration = max(migrations, key=lambda m: m.version)

# Execute the down SQL directly
if last_migration.down_sql:
    # Execute the down SQL to revert the schema changes
    await db.execute(last_migration.down_sql)
    
    # Remove the migration record from the _migrations table
    await db.execute(
        "DELETE FROM _migrations WHERE version = %s",
        (last_migration.version,)
    )
    print(f"Manually reverted migration V{last_migration.version}")
else:
    print(f"No down SQL for migration V{last_migration.version}")
```

### Checking Migration Status

```python
# Get all applied migrations
result = await db.execute(
    "SELECT version, description, applied_at FROM _migrations ORDER BY version"
)
for row in result:
    print(f"Version {row['version']}: {row['description']} (applied at {row['applied_at']})")
```

## Error Handling During Migrations

When working with migrations, it's important to handle errors properly to maintain database consistency.

### Handling Migration Errors

```python
# Synchronous error handling
try:
    migration.migrate()
    print("Migrations applied successfully")
except Exception as e:
    print(f"Error applying migrations: {e}")
    # Implement recovery strategy here
    # For example, you might want to:
    # 1. Log the error
    # 2. Notify administrators
    # 3. Attempt to rollback to a known good state
```

```python
# Asynchronous error handling
try:
    await migration.migrate()
    print("Migrations applied successfully")
except Exception as e:
    print(f"Error applying migrations: {e}")
    # Implement recovery strategy here
```

### Transaction Safety

All migrations are executed within transactions, which means:

1. If a migration fails, all changes from that migration are rolled back
2. The migration table is not updated if the migration fails
3. Subsequent migrations are not applied after a failure

This ensures that your database remains in a consistent state even if a migration fails.

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

## Environment-Specific Migrations

In some cases, you may need to run different migrations in different environments (development, staging, production). Here are some strategies for handling environment-specific migrations:

### Using Environment Variables

```python
import os

# Get current environment
environment = os.environ.get("ENVIRONMENT", "development")

# Create environment-specific migration
if environment == "development":
    migration.create_migration(
        "add_test_data",
        """
        INSERT INTO users (name, email) VALUES
        ('Test User 1', 'test1@example.com'),
        ('Test User 2', 'test2@example.com');
        """,
        """
        DELETE FROM users WHERE email IN ('test1@example.com', 'test2@example.com');
        """
    )
```

### Using Conditional Logic in Migrations

You can also include conditional logic within your migration SQL:

```sql
-- Create different indexes based on environment
DO $$
BEGIN
    IF current_setting('app.environment') = 'production' THEN
        CREATE INDEX idx_users_email ON users (email);
    ELSE
        -- More aggressive indexing for development/testing
        CREATE INDEX idx_users_email ON users (email);
        CREATE INDEX idx_users_name ON users (name);
    END IF;
END $$;
```

### Separate Migration Directories

Another approach is to maintain separate migration directories for different environments:

```python
# Determine migration directory based on environment
environment = os.environ.get("ENVIRONMENT", "development")
migrations_dir = f"./migrations/{environment}"

# Create migration instance with environment-specific directory
migration = Migration(db, migrations_dir=migrations_dir)
```

## Migrations in CI/CD Pipelines

Integrating database migrations into your Continuous Integration and Continuous Deployment (CI/CD) pipelines is essential for automated deployments. Here are some strategies:

### Automated Migration Testing

In your CI pipeline, you can automatically test migrations:

```yaml
# Example GitHub Actions workflow
jobs:
  test-migrations:
    runs-on: ubuntu-latest
    services:
      cockroachdb:
        image: cockroachdb/cockroach:latest
        ports:
          - 26257:26257
        options: --command="start-single-node --insecure"
    
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .
      
      - name: Test migrations
        run: |
          python -m tests.test_migrations
        env:
          DATABASE_URL: postgresql://root@localhost:26257/defaultdb?sslmode=disable
```

### Deployment Strategies

When deploying to production, consider these strategies:

1. **Migration-first deployment**: Apply migrations before deploying new application code
   ```bash
   # Example deployment script
   python -m scripts.apply_migrations
   deploy_application_code
   ```

2. **Blue-Green deployment**: Apply migrations to a new database, then switch the application to use it
   ```bash
   # Create new database with migrations applied
   python -m scripts.create_new_db_with_migrations
   
   # Update application config to point to new database
   update_application_config
   
   # Deploy new application code
   deploy_application_code
   ```

3. **Canary deployment**: Apply migrations, then gradually route traffic to the new version
   ```bash
   # Apply migrations
   python -m scripts.apply_migrations
   
   # Deploy new version to a subset of servers
   deploy_canary
   
   # Monitor and gradually increase traffic to new version
   monitor_and_scale_deployment
   ```

### Rollback Strategies

Always have a rollback strategy for failed migrations:

```python
# Example rollback script
from manticore_cockroachdb import Database, Migration
import os

def rollback_last_migration():
    db = Database.from_url(os.environ["DATABASE_URL"])
    migration = Migration(db)
    
    # Get current version
    current_version = migration.get_current_version()
    print(f"Current version: {current_version}")
    
    # Rollback one migration
    rollback_count = migration.rollback(count=1)
    print(f"Rolled back {rollback_count} migrations")
    
    db.close()

if __name__ == "__main__":
    rollback_last_migration()
```

## Troubleshooting

- **Migration table doesn't exist**: If you get an error about the `_migrations` table not existing, make sure to call `migration.initialize()` or `await migration.initialize()` before applying migrations.
- **Migration version conflict**: If you have conflicts with migration versions, consider using timestamps for version numbers to avoid collisions.
- **SQL syntax errors**: Test your migrations in a development environment before applying them to production.

## Best Practices for Database Migrations

Here are some best practices to follow when working with database migrations:

### 1. Keep Migrations Small and Focused

Each migration should make a small, focused change to the database schema. This makes migrations easier to understand, test, and debug.

### 2. Make Migrations Reversible

Always provide down SQL for your migrations so they can be reversed if needed. This is especially important for production environments.

### 3. Test Migrations Before Applying to Production

Always test migrations in a development or staging environment before applying them to production. This helps catch issues early.

### 4. Use Descriptive Names

Give your migrations descriptive names that clearly indicate what they do. For example, `create_users_table` is better than `update_schema`.

### 5. Include Comments in Complex Migrations

For complex migrations, include comments in the SQL to explain what the migration is doing and why.

### 6. Version Control Your Migrations

Keep your migration files in version control along with your application code. This ensures that all developers have access to the same migrations.

### 7. Avoid Data Loss

Be careful with migrations that modify or delete data. Consider creating backup tables or columns before making destructive changes.

### 8. Use Transactions

Ensure migrations run within transactions to maintain database consistency. The Manticore CockroachDB client handles this automatically.

### 9. Consider Database Performance

For large tables, consider the performance impact of migrations. Some operations (like adding indexes) can lock tables and cause downtime.

### 10. Document Schema Changes

Keep documentation of your database schema up to date as you apply migrations. This helps new team members understand the database structure.

## Performance Considerations for Migrations

When working with large databases, migrations can impact performance. Here are some considerations:

### Minimizing Downtime

For production databases, minimizing downtime during migrations is crucial:

1. **Use Non-Blocking Operations**: When possible, use operations that don't block the entire table.
   ```sql
   -- Instead of this (blocks the table)
   ALTER TABLE users ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT FALSE;
   
   -- Do this (less blocking)
   ALTER TABLE users ADD COLUMN email_verified BOOLEAN;
   UPDATE users SET email_verified = FALSE;
   ALTER TABLE users ALTER COLUMN email_verified SET NOT NULL;
   ```

2. **Batch Large Data Migrations**: For large data migrations, process data in batches.
   ```python
   # Example of batched data migration
   async def migrate_data_in_batches(db, batch_size=1000):
       # Get total count
       result = await db.execute("SELECT COUNT(*) as count FROM users")
       total = result[0]['count']
       
       # Process in batches
       for offset in range(0, total, batch_size):
           await db.execute(
               """
               UPDATE users 
               SET full_name = CONCAT(first_name, ' ', last_name)
               WHERE id IN (
                   SELECT id FROM users ORDER BY id LIMIT %s OFFSET %s
               )
               """,
               (batch_size, offset)
           )
           print(f"Processed {min(offset + batch_size, total)}/{total} records")
   ```

3. **Schedule During Low-Traffic Periods**: Run migrations during periods of low traffic.

### CockroachDB-Specific Optimizations

CockroachDB has specific considerations for schema changes:

1. **Online Schema Changes**: CockroachDB supports online schema changes, but they can still impact performance.

2. **Avoid Long-Running Transactions**: Long-running transactions can cause contention.
   ```python
   # Instead of one large transaction
   async def migrate_in_smaller_transactions(db):
       # Get IDs to process
       ids = await db.execute("SELECT id FROM large_table")
       
       # Process each ID in its own transaction
       for id_batch in chunk_list(ids, 100):
           async def process_batch(conn):
               for id_obj in id_batch:
                   await conn.execute(
                       "UPDATE large_table SET processed = TRUE WHERE id = %s",
                       (id_obj['id'],)
                   )
           await db.run_in_transaction(process_batch)
   
   def chunk_list(lst, chunk_size):
       """Split list into chunks of specified size."""
       return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
   ```

3. **Monitor Query Performance**: Use CockroachDB's monitoring tools to track query performance during migrations.

### Testing Migration Performance

Before running migrations in production, test their performance:

```python
import time

async def test_migration_performance():
    db = AsyncDatabase(database="test_db")
    await db.connect()
    
    # Create test data
    await db.execute("CREATE TABLE test_users (id SERIAL PRIMARY KEY, name TEXT)")
    await db.execute("INSERT INTO test_users (name) SELECT 'User ' || i FROM generate_series(1, 10000) AS i")
    
    # Measure migration time
    start_time = time.time()
    await db.execute("ALTER TABLE test_users ADD COLUMN email TEXT")
    end_time = time.time()
    
    print(f"Migration took {end_time - start_time:.2f} seconds")
    
    # Clean up
    await db.execute("DROP TABLE test_users")
    await db.close()
``` 