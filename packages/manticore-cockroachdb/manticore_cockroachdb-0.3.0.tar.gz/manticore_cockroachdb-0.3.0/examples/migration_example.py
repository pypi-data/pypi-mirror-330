#!/usr/bin/env python3
"""Migration examples for the Manticore CockroachDB client.

This example demonstrates how to work with database migrations:
1. Creating migration files
2. Loading migrations
3. Applying migrations
4. Rolling back migrations

Prerequisites:
- A running CockroachDB server
- The manticore-cockroachdb library installed
"""

import os
import logging
import shutil
from pathlib import Path

from manticore_cockroachdb.database import Database
from manticore_cockroachdb.migration import Migration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run the migration example."""
    # Connect to database - either from environment or defaults
    database_url = os.environ.get("DATABASE_URL")
    
    if database_url:
        logger.info("Connecting to database using DATABASE_URL")
        db = Database.from_url(database_url)
    else:
        logger.info("Connecting to local CockroachDB instance")
        db = Database(database="example_db")
    
    # Setup migrations directory
    migrations_dir = Path("./example_migrations")
    if migrations_dir.exists():
        shutil.rmtree(migrations_dir)
    migrations_dir.mkdir(exist_ok=True)
    
    try:
        # Create migration instance
        migration = Migration(db, migrations_dir=str(migrations_dir))
        
        # Create migration files
        logger.info("Creating migration: Create users table")
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
        
        logger.info("Creating migration: Add age column")
        migration.create_migration(
            "add age column", 
            "ALTER TABLE users ADD COLUMN age INTEGER;",
            "ALTER TABLE users DROP COLUMN age;"
        )
        
        logger.info("Creating migration: Add active flag")
        migration.create_migration(
            "add active flag", 
            "ALTER TABLE users ADD COLUMN active BOOLEAN DEFAULT TRUE;",
            "ALTER TABLE users DROP COLUMN active;"
        )
        
        # List migration files
        logger.info("Migration files created:")
        for file in sorted(migrations_dir.glob("*.sql")):
            logger.info("  {0}".format(file.name))
        
        # Load migrations
        logger.info("Loading migrations")
        migrations = migration.load_migrations()
        logger.info("Loaded {0} migrations".format(len(migrations)))
        
        for m in migrations:
            logger.info("  Version {0}: {1}".format(m.version, m.description))
        
        # Apply migrations
        logger.info("Applying migrations")
        applied = migration.migrate()
        logger.info("Applied {0} migrations".format(applied))
        
        # Check if migrations table exists and show applied migrations
        results = db.execute("SELECT version, description, applied_at FROM _migrations ORDER BY version")
        if results:
            logger.info("Applied migrations in database:")
            for row in results:
                logger.info("  Version {0}: {1} (applied at {2})".format(row['version'], row['description'], row['applied_at']))
        
        # Insert test data
        logger.info("Inserting test user")
        db.insert("users", {
            "name": "Migration Test User",
            "email": "migrate@example.com",
            "age": 30
        })
        
        # Show user data
        users = db.select("users")
        logger.info("Users in database: {0}".format(len(users)))
        for user in users:
            logger.info("  {0} (age: {1}, active: {2})".format(user['name'], user['age'], user['active']))
        
        # Rollback last migration
        logger.info("Rolling back last migration")
        rollback_count = migration.rollback(count=1)
        logger.info("Rolled back {0} migrations".format(rollback_count))
        
        # Show schema after rollback
        try:
            # Check if active column still exists (should be gone)
            db.execute("SELECT active FROM users LIMIT 1")
            logger.info("Active column still exists (rollback failed)")
        except Exception:
            logger.info("Active column removed successfully (rollback worked)")
        
        # Apply all migrations again
        logger.info("Applying all migrations again")
        applied = migration.migrate()
        logger.info("Applied {0} migrations".format(applied))
        
    finally:
        # Clean up
        logger.info("Cleaning up")
        try:
            db.drop_table("users", if_exists=True)
            db.drop_table("_migrations", if_exists=True)
        except Exception as e:
            logger.error("Error during cleanup: {0}".format(e))
        
        # Close database connection
        logger.info("Closing database connection")
        db.close()
        
        # Remove migrations directory
        logger.info("Removing migrations directory")
        shutil.rmtree(migrations_dir)


if __name__ == "__main__":
    main() 