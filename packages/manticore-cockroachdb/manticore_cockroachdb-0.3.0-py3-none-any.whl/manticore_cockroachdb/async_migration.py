"""Asynchronous schema migration support for CockroachDB.

This module provides tools for managing database schema migrations asynchronously.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .async_database import AsyncDatabase

logger = logging.getLogger(__name__)


class AsyncMigration:
    """Asynchronous database migration."""
    
    def __init__(
        self,
        version: int,
        description: str,
        up_sql: str,
        down_sql: Optional[str] = None
    ):
        """Initialize migration.
        
        Args:
            version: Migration version number
            description: Migration description
            up_sql: SQL to apply migration
            down_sql: SQL to revert migration
        """
        self.version = version
        self.description = description
        self.up_sql = up_sql
        self.down_sql = down_sql


class AsyncMigrator:
    """Asynchronous database schema migrator."""
    
    def __init__(self, db: AsyncDatabase, migrations_dir: str = "migrations"):
        """Initialize migrator.
        
        Args:
            db: AsyncDatabase instance
            migrations_dir: Directory containing migration files
        """
        self.db = db
        self.migrations_dir = migrations_dir
    
    async def initialize(self) -> None:
        """Initialize migrator and ensure migrations table exists."""
        await self._ensure_migrations_table()
        
    async def _ensure_migrations_table(self) -> None:
        """Create migrations table if it doesn't exist."""
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS _migrations (
                version INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                applied_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    
    async def get_applied_versions(self) -> List[int]:
        """Get list of applied migration versions.
        
        Returns:
            List of applied version numbers
        """
        result = await self.db.execute(
            "SELECT version FROM _migrations ORDER BY version"
        )
        return [row["version"] for row in result]
    
    async def load_migrations(self) -> List[AsyncMigration]:
        """Load migrations from migrations directory.
        
        Returns:
            List of migrations
        """
        migrations = []
        migrations_path = Path(self.migrations_dir)
        
        if not migrations_path.exists():
            logger.warning(f"Migrations directory {self.migrations_dir} does not exist")
            return migrations
        
        # Get all SQL files
        sql_files = sorted(migrations_path.glob("V*__*.sql"))
        
        for file_path in sql_files:
            try:
                # Parse version and description from filename
                # Filename format: V{version}__{description}.sql
                file_name = file_path.name
                version_part, description_part = file_name.split("__", 1)
                version = int(version_part[1:])  # Remove 'V' prefix
                description = description_part.split(".")[0].replace("_", " ")
                
                # Read SQL file
                with open(file_path, "r") as f:
                    up_sql = f.read()
                
                # Check for down migration
                down_path = file_path.with_name(f"U{version_part[1:]}__undo_{description_part}")
                down_sql = None
                if down_path.exists():
                    with open(down_path, "r") as f:
                        down_sql = f.read()
                
                # Create migration
                migration = AsyncMigration(
                    version=version,
                    description=description,
                    up_sql=up_sql,
                    down_sql=down_sql
                )
                migrations.append(migration)
                logger.debug(f"Loaded migration V{version}: {description}")
                
            except Exception as e:
                logger.error(f"Failed to load migration {file_path}: {e}")
                
        return sorted(migrations, key=lambda m: m.version)
    
    async def create_migration(
        self,
        description: str,
        up_sql: str,
        down_sql: Optional[str] = None
    ) -> None:
        """Create a new migration file.
        
        Args:
            description: Migration description
            up_sql: SQL to apply migration
            down_sql: SQL to revert migration
        """
        migrations_path = Path(self.migrations_dir)
        
        # Create migrations directory if it doesn't exist
        if not migrations_path.exists():
            migrations_path.mkdir(parents=True)
            logger.info(f"Created migrations directory {self.migrations_dir}")
        
        # Get next version number
        applied_versions = await self.get_applied_versions()
        loaded_migrations = await self.load_migrations()
        loaded_versions = [m.version for m in loaded_migrations]
        all_versions = set(applied_versions + loaded_versions)
        
        next_version = 1
        if all_versions:
            next_version = max(all_versions) + 1
        
        # Format description for filename
        file_description = description.lower().replace(" ", "_")
        
        # Create migration file
        file_path = migrations_path / f"V{next_version}__{file_description}.sql"
        with open(file_path, "w") as f:
            f.write(up_sql)
        logger.info(f"Created migration V{next_version}: {description}")
        
        # Create undo migration file if provided
        if down_sql:
            down_path = migrations_path / f"U{next_version}__undo_{file_description}.sql"
            with open(down_path, "w") as f:
                f.write(down_sql)
            logger.info(f"Created undo migration U{next_version}")
    
    async def migrate(self, target_version: Optional[int] = None) -> None:
        """Apply or revert migrations to reach target version.
        
        Args:
            target_version: Target version to migrate to.
                If None, migrate to latest version.
                If lower than current version, revert migrations.
        """
        # Ensure migrations table exists
        await self._ensure_migrations_table()
        
        # Get applied migrations
        applied_versions = await self.get_applied_versions()
        current_version = max(applied_versions) if applied_versions else 0
        
        # Load migrations
        all_migrations = await self.load_migrations()
        available_versions = [m.version for m in all_migrations]
        
        # Determine target version
        if target_version is None:
            # Migrate to latest version
            target_version = max(available_versions) if available_versions else 0
        
        # Nothing to do if we're already at the target version
        if current_version == target_version:
            logger.info(f"Already at target version {target_version}")
            return
        
        logger.info(f"Migrating from version {current_version} to {target_version}")
        
        if target_version > current_version:
            # Apply migrations up to target version
            migrations_to_apply = [
                m for m in all_migrations
                if m.version > current_version and m.version <= target_version
            ]
            
            logger.info(f"Applying {len(migrations_to_apply)} migrations")
            
            for migration in migrations_to_apply:
                logger.info(f"Applying migration V{migration.version}: {migration.description}")
                try:
                    # Run migration in transaction
                    async def apply_migration(conn):
                        async with conn.cursor() as cur:
                            await cur.execute(migration.up_sql)
                            await cur.execute(
                                "INSERT INTO _migrations (version, description) VALUES (%s, %s)",
                                (migration.version, migration.description)
                            )
                        return None
                    
                    await self.db.run_in_transaction(apply_migration)
                    logger.info(f"Applied migration V{migration.version}")
                    
                except Exception as e:
                    logger.error(f"Failed to apply migration V{migration.version}: {e}")
                    raise
        else:
            # Revert migrations down to target version
            migrations_to_revert = [
                m for m in all_migrations
                if m.version > target_version and m.version <= current_version
            ]
            
            # Sort migrations in reverse order for reverting
            migrations_to_revert.sort(key=lambda m: m.version, reverse=True)
            
            logger.info(f"Reverting {len(migrations_to_revert)} migrations")
            
            for migration in migrations_to_revert:
                if not migration.down_sql:
                    logger.error(f"Cannot revert migration V{migration.version}: No down SQL")
                    raise ValueError(f"Cannot revert migration V{migration.version}: No down SQL")
                
                logger.info(f"Reverting migration V{migration.version}: {migration.description}")
                try:
                    # Run revert in transaction
                    async def revert_migration(conn):
                        async with conn.cursor() as cur:
                            await cur.execute(migration.down_sql)
                            await cur.execute(
                                "DELETE FROM _migrations WHERE version = %s",
                                (migration.version,)
                            )
                        return None
                    
                    await self.db.run_in_transaction(revert_migration)
                    logger.info(f"Reverted migration V{migration.version}")
                    
                except Exception as e:
                    logger.error(f"Failed to revert migration V{migration.version}: {e}")
                    raise
        
        logger.info(f"Migration to version {target_version} completed") 