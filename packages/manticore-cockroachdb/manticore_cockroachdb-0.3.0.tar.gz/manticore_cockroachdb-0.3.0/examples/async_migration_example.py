#!/usr/bin/env python3
"""Async migration examples for the Manticore CockroachDB client.

This example demonstrates how to work with async database migrations:
1. Creating migration files
2. Loading migrations
3. Applying migrations asynchronously 
4. Rolling back migrations asynchronously

Prerequisites:
- A running CockroachDB server
- The manticore-cockroachdb library installed
"""

import os
import asyncio
import logging
import shutil
from pathlib import Path

from manticore_cockroachdb.async_database import AsyncDatabase
from manticore_cockroachdb.async_migration import AsyncMigration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Run the async migration example."""
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
        migration = AsyncMigration(db, migrations_dir=str(migrations_dir))
        
        # Create migration files
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
        logger.info("Migration files created:")
        for file in sorted(migrations_dir.glob("*.sql")):
            logger.info("  {0}".format(file.name))
        
        # Load migrations
        logger.info("Loading migrations")
        migrations = await migration.load_migrations()
        logger.info("Loaded {0} migrations".format(len(migrations)))
        
        for m in migrations:
            logger.info("  Version {0}: {1}".format(m.version, m.description))
        
        # Apply migrations
        logger.info("Applying migrations")
        applied = await migration.migrate()
        logger.info("Applied {0} migrations".format(applied))
        
        # Check if migrations table exists and show applied migrations
        results = await db.execute("SELECT version, description, applied_at FROM _async_migrations ORDER BY version")
        if results:
            logger.info("Applied migrations in database:")
            for row in results:
                logger.info("  Version {0}: {1} (applied at {2})".format(row['version'], row['description'], row['applied_at']))
        
        # Insert test data
        logger.info("Inserting test user")
        await db.insert("async_users", {
            "name": "Async Migration Test User",
            "email": "async_migrate@example.com",
            "email_verified": True,
            "bio": "This is a test user created during migration.",
            "avatar_url": "https://example.com/avatar.png"
        })
        
        # Show user data
        users = await db.select("async_users")
        logger.info("Users in database: {0}".format(len(users)))
        for user in users:
            logger.info("  {0} - Email: {1} (verified: {2})".format(user['name'], user['email'], user['email_verified']))
            logger.info("    Bio: {0}".format(user['bio']))
            logger.info("    Avatar: {0}".format(user['avatar_url']))
        
        # Rollback last migration
        logger.info("Rolling back last migration")
        rollback_count = await migration.rollback(count=1)
        logger.info("Rolled back {0} migrations".format(rollback_count))
        
        # Show schema after rollback
        try:
            # Check if bio column still exists (should be gone)
            await db.execute("SELECT bio FROM async_users LIMIT 1")
            logger.info("Bio column still exists (rollback failed)")
        except Exception:
            logger.info("Bio column removed successfully (rollback worked)")
        
        # Apply all migrations again
        logger.info("Applying all migrations again")
        applied = await migration.migrate()
        logger.info("Applied {0} migrations".format(applied))
        
    finally:
        # Clean up
        logger.info("Cleaning up")
        try:
            await db.drop_table("async_users", if_exists=True)
            await db.drop_table("_async_migrations", if_exists=True)
        except Exception as e:
            logger.error("Error during cleanup: {0}".format(e))
        
        # Close database connection
        logger.info("Closing database connection")
        await db.close()
        
        # Remove migrations directory
        logger.info("Removing migrations directory")
        shutil.rmtree(migrations_dir)


if __name__ == "__main__":
    asyncio.run(main()) 