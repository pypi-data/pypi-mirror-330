"""Schema migration support for CockroachDB.

This module provides tools for managing database schema migrations.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .database import Database

logger = logging.getLogger(__name__)


class Migration:
    """Database migration."""
    
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


class Migrator:
    """Database schema migrator."""
    
    def __init__(self, db: Database, migrations_dir: str = "migrations"):
        """Initialize migrator.
        
        Args:
            db: Database instance
            migrations_dir: Directory containing migration files
        """
        self.db = db
        self.migrations_dir = migrations_dir
        self._ensure_migrations_table()
    
    def _ensure_migrations_table(self) -> None:
        """Create migrations table if it doesn't exist."""
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS _migrations (
                version INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                applied_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    
    def get_applied_versions(self) -> List[int]:
        """Get list of applied migration versions.
        
        Returns:
            List of applied migration version numbers
        """
        results = self.db.execute(
            "SELECT version FROM _migrations ORDER BY version"
        )
        return [r["version"] for r in results]
    
    def load_migrations(self) -> List[Migration]:
        """Load migrations from migrations directory.
        
        Returns:
            List of migrations
        """
        migrations = []
        migrations_dir = Path(self.migrations_dir)
        
        if not migrations_dir.exists():
            return migrations
            
        for file in sorted(migrations_dir.glob("*.sql")):
            # Parse filename: V<version>__<description>.sql
            if not file.name.startswith("V"):
                continue
                
            try:
                version_str = file.name[1:].split("__")[0]
                version = int(version_str)
                description = file.name.split("__")[1].replace(".sql", "")
                
                # Read migration SQL
                with open(file) as f:
                    content = f.read()
                    
                # Split into up/down migrations if separator exists
                parts = content.split("\n-- DOWN\n")
                up_sql = parts[0].strip()
                down_sql = parts[1].strip() if len(parts) > 1 else None
                
                migrations.append(
                    Migration(version, description, up_sql, down_sql)
                )
            except Exception as e:
                logger.error(f"Failed to load migration {file}: {e}")
                continue
                
        return sorted(migrations, key=lambda m: m.version)
    
    def create_migration(
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
        migrations_dir = Path(self.migrations_dir)
        migrations_dir.mkdir(exist_ok=True)
        
        # Get next version number
        existing = self.load_migrations()
        version = 1
        if existing:
            version = max(m.version for m in existing) + 1
            
        # Create migration file
        filename = f"V{version}__{description}.sql"
        path = migrations_dir / filename
        
        content = up_sql.strip()
        if down_sql:
            content += f"\n\n-- DOWN\n{down_sql.strip()}"
            
        with open(path, "w") as f:
            f.write(content)
            
        logger.info(f"Created migration {filename}")
    
    def migrate(self, target_version: Optional[int] = None) -> None:
        """Apply pending migrations.
        
        Args:
            target_version: Target version to migrate to.
                If None, applies all pending migrations.
        """
        # Get current state
        applied = self.get_applied_versions()
        migrations = self.load_migrations()
        
        if not migrations:
            logger.info("No migrations found")
            return
            
        if target_version is None:
            target_version = max(m.version for m in migrations)
            
        current_version = max(applied) if applied else 0
        
        if target_version == current_version:
            logger.info(f"Already at version {target_version}")
            return
            
        # Determine migrations to apply/revert
        if target_version > current_version:
            # Apply migrations
            to_apply = [
                m for m in migrations
                if m.version > current_version and m.version <= target_version
            ]
            
            for migration in to_apply:
                logger.info(
                    f"Applying migration V{migration.version}: {migration.description}"
                )
                try:
                    def apply_migration(conn):
                        with conn.cursor() as cur:
                            # Apply migration
                            cur.execute(migration.up_sql)
                            # Record migration
                            cur.execute(
                                """
                                INSERT INTO _migrations (version, description)
                                VALUES (%s, %s)
                                """,
                                (migration.version, migration.description)
                            )
                    
                    self.db.run_in_transaction(apply_migration)
                    logger.info("Migration applied successfully")
                except Exception as e:
                    logger.error(f"Migration failed: {e}")
                    raise
        else:
            # Revert migrations
            to_revert = [
                m for m in reversed(migrations)
                if m.version <= current_version and m.version > target_version
            ]
            
            for migration in to_revert:
                if not migration.down_sql:
                    raise ValueError(
                        f"Migration V{migration.version} cannot be reverted: "
                        "no down migration provided"
                    )
                    
                logger.info(
                    f"Reverting migration V{migration.version}: {migration.description}"
                )
                try:
                    def revert_migration(conn):
                        with conn.cursor() as cur:
                            # Revert migration
                            cur.execute(migration.down_sql)
                            # Remove migration record
                            cur.execute(
                                "DELETE FROM _migrations WHERE version = %s",
                                (migration.version,)
                            )
                    
                    self.db.run_in_transaction(revert_migration)
                    logger.info("Migration reverted successfully")
                except Exception as e:
                    logger.error(f"Migration revert failed: {e}")
                    raise 