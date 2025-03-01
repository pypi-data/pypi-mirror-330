#!/usr/bin/env python3
"""Async migration examples for the Manticore CockroachDB client.

This example demonstrates how to work with asynchronous database migrations:
1. Creating migration files with up and down SQL scripts
2. Loading migrations from the filesystem
3. Applying migrations to update the database schema
4. Reverting migrations using both built-in and manual methods
5. Checking migration status and history

Prerequisites:
- A running CockroachDB server
- The manticore-cockroachdb library installed

Key concepts demonstrated:
- AsyncMigrator for managing database schema changes
- Migration versioning and tracking
- Forward and backward schema changes
- Multiple methods for reverting migrations
- Error handling during migration operations
"""

import os
import asyncio
import logging
import shutil
from pathlib import Path

from manticore_cockroachdb.async_database import AsyncDatabase
from manticore_cockroachdb.async_migration import AsyncMigrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Run the async migration example.
    
    This function demonstrates the complete lifecycle of async migrations:
    - Connecting to the database
    - Creating migration files
    - Applying migrations
    - Inserting test data
    - Reverting migrations using built-in method
    - Reverting migrations using manual method
    - Reapplying migrations
    - Cleaning up resources
    """
    # Connect to database - either from environment or defaults
    database_url = os.environ.get("DATABASE_URL")
    
    if database_url:
        logger.info("Connecting to database using DATABASE_URL")
        db = AsyncDatabase.from_url(database_url)
    else:
        logger.info("Connecting to local CockroachDB instance")
        db = AsyncDatabase(database="example_db")
    
    # Connect to database
    await db.connect()
    
    # Setup migrations directory
    migrations_dir = Path("./async_example_migrations")
    if migrations_dir.exists():
        shutil.rmtree(migrations_dir)
    migrations_dir.mkdir(exist_ok=True)
    
    try:
        # Create migration instance
        migration = AsyncMigrator(db, migrations_dir=str(migrations_dir))
        
        # Ensure migrations table exists
        # This creates the _migrations table if it doesn't exist
        logger.info("Ensuring migrations table exists")
        await migration.initialize()
        
        # Create migration files
        # Each migration has:
        # - A version number (automatically assigned)
        # - A description
        # - Up SQL (to apply the migration)
        # - Down SQL (to revert the migration)
        
        logger.info("Creating migration: Create async users table")
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
        
        logger.info("Creating migration: Add email verification")
        await migration.create_migration(
            "add email verification", 
            "ALTER TABLE async_users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;",
            "ALTER TABLE async_users DROP COLUMN email_verified;"
        )
        
        logger.info("Creating migration: Add profile fields")
        await migration.create_migration(
            "add profile fields", 
            """
            ALTER TABLE async_users ADD COLUMN bio TEXT;
            ALTER TABLE async_users ADD COLUMN avatar_url TEXT;
            """,
            """
            ALTER TABLE async_users DROP COLUMN bio;
            ALTER TABLE async_users DROP COLUMN avatar_url;
            """
        )
        
        # List migration files
        # Migration files follow the naming convention:
        # - V{version}__{description}.sql for up migrations
        # - U{version}__undo_{description}.sql for down migrations
        logger.info("Migration files created:")
        for file in sorted(migrations_dir.glob("*.sql")):
            logger.info("  {0}".format(file.name))
        
        # Load migrations from the filesystem
        logger.info("Loading migrations")
        migrations = await migration.load_migrations()
        logger.info("Loaded {0} migrations".format(len(migrations)))
        
        for m in migrations:
            logger.info("  Version {0}: {1}".format(m.version, m.description))
        
        # Apply migrations
        # This will apply all migrations that haven't been applied yet
        # Migrations are applied in order of version number
        logger.info("Applying migrations")
        try:
            await migration.migrate()
            logger.info("Migrations applied successfully")
        except Exception as e:
            logger.error(f"Error applying migrations: {e}")
        
        # Check migration history in the database
        # The _migrations table tracks which migrations have been applied
        results = await db.execute("SELECT version, description, applied_at FROM _migrations ORDER BY version")
        if results:
            logger.info("Applied migrations in database:")
            for row in results:
                logger.info("  Version {0}: {1} (applied at {2})".format(row['version'], row['description'], row['applied_at']))
        
        # Insert test data to demonstrate the schema is working
        logger.info("Inserting test user")
        await db.insert("async_users", {
            "name": "Async Migration Test User",
            "email": "async_migrate@example.com",
            "email_verified": True,
            "bio": "This is a test user created during migration.",
            "avatar_url": "https://example.com/avatar.png"
        })
        
        # Show user data to verify all columns were created correctly
        users = await db.select("async_users")
        logger.info("Users in database: {0}".format(len(users)))
        for user in users:
            logger.info("  {0} - Email: {1} (verified: {2})".format(user['name'], user['email'], user['email_verified']))
            logger.info("    Bio: {0}".format(user['bio']))
            logger.info("    Avatar: {0}".format(user['avatar_url']))
        
        # Method 1: Revert using the built-in migrate method
        # This demonstrates how to revert to a specific version using the migrate method
        logger.info("Reverting to version 2 using migrate method")
        try:
            # This will revert the last migration (version 3)
            await migration.migrate(target_version=2)
            logger.info("Reverted to version 2 successfully")
            
            # Verify the migration was reverted
            try:
                # Check if bio column still exists (should be gone)
                await db.execute("SELECT bio FROM async_users LIMIT 1")
                logger.error("Bio column still exists (revert failed)")
            except Exception:
                logger.info("Bio column removed successfully (revert worked)")
        except Exception as e:
            logger.error(f"Error reverting migration: {e}")
        
        # Method 2: Manual migration reversion
        # This demonstrates how to manually revert a migration
        logger.info("Manually reverting version 2")
        try:
            # Get migration version 2
            migration_to_revert = next((m for m in migrations if m.version == 2), None)
            
            if migration_to_revert and migration_to_revert.down_sql:
                # Execute the down SQL directly
                await db.execute(migration_to_revert.down_sql)
                
                # Remove the migration record from the _migrations table
                await db.execute(
                    "DELETE FROM _migrations WHERE version = %s",
                    (migration_to_revert.version,)
                )
                logger.info(f"Manually reverted migration V{migration_to_revert.version}")
                
                # Verify the migration was reverted
                try:
                    # Check if email_verified column still exists (should be gone)
                    await db.execute("SELECT email_verified FROM async_users LIMIT 1")
                    logger.error("email_verified column still exists (manual revert failed)")
                except Exception:
                    logger.info("email_verified column removed successfully (manual revert worked)")
            else:
                logger.warning(f"No migration with version 2 found or no down SQL available")
        except Exception as e:
            logger.error(f"Error manually reverting migration: {e}")
        
        # Reapply all migrations
        # This demonstrates that migrations can be reapplied after being reverted
        logger.info("Applying all migrations again")
        try:
            await migration.migrate()
            logger.info("Migrations reapplied successfully")
            
            # Verify migrations were reapplied
            results = await db.execute("SELECT version, description FROM _migrations ORDER BY version")
            if results:
                logger.info("Current migrations in database:")
                for row in results:
                    logger.info(f"  Version {row['version']}: {row['description']}")
        except Exception as e:
            logger.error(f"Error reapplying migrations: {e}")
        
    finally:
        # Clean up all resources
        logger.info("Cleaning up")
        try:
            # Drop tables created during the example
            await db.drop_table("async_users", if_exists=True)
            await db.drop_table("_migrations", if_exists=True)
        except Exception as e:
            logger.error("Error during cleanup: {0}".format(e))
        
        # Close database connection
        logger.info("Closing database connection")
        await db.close()
        
        # Remove migrations directory
        logger.info("Removing migrations directory")
        shutil.rmtree(migrations_dir)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 