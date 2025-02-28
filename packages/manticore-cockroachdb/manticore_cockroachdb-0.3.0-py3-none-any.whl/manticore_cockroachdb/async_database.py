"""Asynchronous CockroachDB database management.

This module provides a high-level asynchronous interface for managing CockroachDB databases.
"""

import asyncio
import logging
import os
import random
import time
from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from urllib.parse import parse_qs, urlparse

import psycopg
import psycopg_pool
from psycopg.errors import SerializationFailure
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type variable for transaction return type
T = TypeVar('T')


class AsyncTransaction:
    """Asynchronous database transaction context manager."""

    def __init__(self, conn: psycopg.AsyncConnection):
        """Initialize transaction.
        
        Args:
            conn: Asynchronous database connection
        """
        self.conn = conn
        self._committed = False
        self._rolledback = False

    async def __aenter__(self) -> psycopg.AsyncConnection:
        """Enter transaction context."""
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit transaction context.
        
        Commits if no exception occurred, otherwise rolls back.
        """
        if exc_type is not None:
            if not self._rolledback:
                await self.conn.rollback()
                self._rolledback = True
        else:
            if not self._committed and not self._rolledback:
                await self.conn.commit()
                self._committed = True

    async def commit(self) -> None:
        """Commit transaction."""
        await self.conn.commit()
        self._committed = True

    async def rollback(self) -> None:
        """Roll back transaction."""
        await self.conn.rollback()
        self._rolledback = True


class AsyncDatabase:
    """Main interface for asynchronous CockroachDB operations."""
    
    def __init__(
        self,
        database: str = "defaultdb",
        host: str = "localhost",
        port: int = 26257,
        user: str = "root",
        password: Optional[str] = None,
        sslmode: str = "disable",
        min_connections: int = 2,
        max_connections: int = 10,
        application_name: str = "manticore-async-db"
    ):
        """Initialize database connection.
        
        Args:
            database: Database name
            host: Database host
            port: Database port
            user: Database user
            password: Database password
            sslmode: SSL mode (disable, verify-ca, verify-full)
            min_connections: Minimum number of connections in pool
            max_connections: Maximum number of connections in pool
            application_name: Application name for connection
        """
        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.sslmode = sslmode
        self.min_connections = min_connections
        self.max_connections = max_connections
        self.application_name = application_name
        
        # Build connection string
        self.dsn = self._build_dsn()
        
        # Initialize connection pool
        self._pool = None
        self._pool_manager = None
    
    def _build_dsn(self) -> str:
        """Build database connection string.
        
        Returns:
            Database connection string
        """
        # Start with required components
        dsn = f"postgresql://{self.user}"
        
        # Add password if provided
        if self.password:
            dsn += f":{self.password}"
            
        # Add host and database
        dsn += f"@{self.host}:{self.port}/{self.database}"
        
        # Add SSL mode
        dsn += f"?sslmode={self.sslmode}"
        
        return dsn
    
    async def connect(self):
        """Connect to database."""
        if self._pool:
            return  # Already connected
        
        logger.info(
            f"Connecting to database {self.database} with pool size {self.min_connections}-{self.max_connections}"
        )
        
        try:
            # Create connection string
            conn_str = (
                f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/"
                f"{self.database}?sslmode={self.sslmode}"
            )
            
            # Create connection pool
            self._pool = AsyncConnectionPool(
                conn_str,
                min_size=self.min_connections,
                max_size=self.max_connections,
                kwargs={"row_factory": dict_row}
            )
            
            # Test connection
            async with self._pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT 1")
            
            logger.info(f"Connected to database {self.database} with pool size {self.min_connections}-{self.max_connections}")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            if self._pool:
                await self._pool.close()
                self._pool = None
            raise
    
    async def close(self) -> None:
        """Close database connection pool."""
        if self._pool:
            try:
                await self._pool.__aexit__(None, None, None)
            finally:
                self._pool = None
                self._pool_manager = None
                logger.info("Closed database connection pool")
    
    async def execute(
        self,
        query: str,
        params: Optional[tuple] = None,
        fetch: bool = True
    ) -> Optional[List[Dict[str, Any]]]:
        """Execute a query and optionally return results.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            fetch: Whether to return results
            
        Returns:
            Query results if fetch=True, None otherwise
        """
        if not self._pool:
            await self.connect()
            
        async with self._pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                if fetch:
                    try:
                        results = await cur.fetchall()
                        await conn.commit()
                        return results
                    except psycopg.ProgrammingError:
                        # No results to fetch (e.g. for DDL statements)
                        await conn.commit()
                        return None
                else:
                    await conn.commit()
                    return None
    
    async def create_database(self, name: str) -> None:
        """Create a new database.
        
        Args:
            name: Database name
        """
        # Connect to default database
        async with AsyncConnectionPool(
            f"postgresql://{self.user}"
            f"{':{}'.format(self.password) if self.password else ''}"
            f"@{self.host}:{self.port}/defaultdb"
            f"?sslmode={self.sslmode}",
            min_size=1,
            max_size=1
        ) as pool:
            async with pool.connection() as conn:
                # Check if database exists
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT datname FROM pg_database WHERE datname = %s",
                        (name,)
                    )
                    if await cur.fetchone():
                        logger.info(f"Database {name} already exists")
                        return
                    
                    # Create database
                    # Use connection.execute instead of cursor to avoid transaction
                    await conn.execute(f'CREATE DATABASE "{name}"')
                    logger.info(f"Created database {name}")
    
    async def create_table(
        self,
        name: str,
        columns: Dict[str, str],
        if_not_exists: bool = True
    ) -> None:
        """Create a new table.
        
        Args:
            name: Table name
            columns: Column definitions {name: type}
            if_not_exists: Whether to create table only if it doesn't exist
        """
        # Build column definitions
        col_defs = ", ".join(f"{col} {type_}" for col, type_ in columns.items())
        
        # Build query
        query = f"CREATE TABLE {'IF NOT EXISTS' if if_not_exists else ''} {name} ({col_defs})"
        
        # Execute query
        await self.execute(query, fetch=False)
        logger.info(f"Created table {name}")
    
    async def drop_table(self, name: str, if_exists: bool = True) -> None:
        """Drop a table.
        
        Args:
            name: Table name
            if_exists: Whether to drop table only if it exists
        """
        # Build query
        query = f"DROP TABLE {'IF EXISTS' if if_exists else ''} {name}"
        
        # Execute query
        await self.execute(query, fetch=False)
        logger.info(f"Dropped table {name}")
    
    async def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a record.
        
        Args:
            table: Table name
            data: Record data
            
        Returns:
            Inserted record
        """
        # Build column list
        columns = ", ".join(data.keys())
        
        # Build parameter placeholders
        placeholders = ", ".join(f"%s" for _ in data)
        
        # Build query
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
        
        # Execute query
        result = await self.execute(query, tuple(data.values()))
        return result[0]
    
    async def select(
        self,
        table: str,
        columns: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Select records from a table.
        
        Args:
            table: Table name
            columns: Columns to select
            where: Where conditions {column: value}
            order_by: Order by clause
            limit: Result limit
            
        Returns:
            Selected records
        """
        # Build query
        cols = "*" if not columns else ", ".join(columns)
        query = f'SELECT {cols} FROM "{table}"'
        
        # Add where clause
        params = []
        if where:
            conditions = []
            for col, value in where.items():
                conditions.append(f"{col} = %s")
                params.append(value)
            query += f" WHERE {' AND '.join(conditions)}"
        
        # Add order by
        if order_by:
            query += f" ORDER BY {order_by}"
            
        # Add limit
        if limit:
            query += f" LIMIT {limit}"
        
        # Execute query
        return await self.execute(query, tuple(params) if params else None)
    
    async def update(
        self,
        table: str,
        data: Dict[str, Any],
        where: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update records.
        
        Args:
            table: Table name
            data: Update data
            where: Filter conditions
            
        Returns:
            Updated record
        """
        # Build update expressions
        updates = []
        update_params = []
        for key, value in data.items():
            updates.append(f"{key} = %s")
            update_params.append(value)
        
        # Build where conditions
        conditions = []
        where_params = []
        for key, value in where.items():
            conditions.append(f"{key} = %s")
            where_params.append(value)
        
        # Build query
        query = f"UPDATE {table} SET {', '.join(updates)} WHERE {' AND '.join(conditions)} RETURNING *"
        
        # Execute query
        result = await self.execute(query, tuple(update_params + where_params))
        return result[0] if result else None
    
    async def delete(
        self,
        table: str,
        where: Dict[str, Any]
    ) -> bool:
        """Delete records.
        
        Args:
            table: Table name
            where: Filter conditions
            
        Returns:
            Whether any records were deleted
        """
        # Build where conditions
        conditions = []
        params = []
        for key, value in where.items():
            conditions.append(f"{key} = %s")
            params.append(value)
        
        # Build query
        query = f"DELETE FROM {table} WHERE {' AND '.join(conditions)}"
        
        # Execute query
        before = await self.execute(f"SELECT COUNT(*) as count FROM {table} WHERE {' AND '.join(conditions)}", tuple(params))
        await self.execute(query, tuple(params), fetch=False)
        
        # Return whether any records were deleted
        return before[0]["count"] > 0 if before else False
    
    @classmethod
    def from_url(cls, url: str) -> 'AsyncDatabase':
        """Create database instance from URL.
        
        Args:
            url: Database URL
            
        Returns:
            Database instance
        """
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        db = cls(
            database=parsed.path.lstrip('/'),
            host=parsed.hostname or "localhost",
            port=parsed.port or 26257,
            user=parsed.username or "root",
            password=parsed.password,
            sslmode=params.get('sslmode', ['disable'])[0]
        )
        
        # Don't connect here, as we'll connect explicitly after creation
        return db
    
    async def __aenter__(self) -> 'AsyncDatabase':
        """Enter context."""
        if not self._pool:
            await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context."""
        await self.close()
    
    async def transaction(self) -> AsyncTransaction:
        """Start a transaction.
        
        Returns:
            Transaction context manager
        """
        if not self._pool:
            await self.connect()
            
        conn = await self._pool.connection()
        return AsyncTransaction(conn)
    
    async def run_in_transaction(
        self,
        operation: Callable[[psycopg.AsyncConnection], T],
        max_retries: int = 3
    ) -> T:
        """Run an operation in a transaction with retry logic.
        
        Args:
            operation: Operation to run
            max_retries: Maximum number of retry attempts
            
        Returns:
            Operation result
            
        Raises:
            ValueError: If transaction fails after max retries
        """
        if not self._pool:
            raise RuntimeError("Database not connected")
        
        async with self._pool.connection() as conn:
            for retry in range(max_retries):
                try:
                    async with AsyncTransaction(conn) as tx_conn:
                        result = await operation(tx_conn)
                        return result
                except SerializationFailure as e:
                    if retry == max_retries - 1:
                        raise ValueError(
                            f"Transaction failed after {max_retries} retries: {e}"
                        )
                    # Exponential backoff
                    sleep_ms = (2 ** retry) * 100 * (random.random() + 0.5)
                    await asyncio.sleep(sleep_ms / 1000)
                    continue
            
            # This should never be reached, but just in case
            raise ValueError(f"Transaction failed after {max_retries} retries")
    
    async def batch_insert(
        self, 
        table: str, 
        records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Insert multiple records into a table.
        
        Args:
            table: Table name
            records: Records to insert
            
        Returns:
            Inserted records
        """
        if not records:
            return []
            
        # Ensure all records have the same keys
        keys = set(records[0].keys())
        for record in records:
            if set(record.keys()) != keys:
                raise ValueError("All records must have the same keys")
        
        # Build query
        columns = list(keys)
        placeholders = ", ".join([
            f"({', '.join(['%s'] * len(columns))})" 
            for _ in range(len(records))
        ])
        query = f"""
            INSERT INTO "{table}" ({", ".join(columns)})
            VALUES {placeholders}
            RETURNING *
        """
        
        # Flatten values
        values = []
        for record in records:
            for col in columns:
                values.append(record[col])
        
        # Execute query
        results = await self.execute(query, tuple(values))
        return results
    
    async def batch_update(
        self, 
        table: str, 
        records: List[Dict[str, Any]], 
        key_column: str = "id"
    ) -> List[Dict[str, Any]]:
        """Update multiple records in a table.
        
        Args:
            table: Table name
            records: Records to update
            key_column: Primary key column
            
        Returns:
            Updated records
        """
        if not records:
            return []
            
        # Ensure all records have the key column and at least one more column
        for record in records:
            if key_column not in record:
                raise ValueError(f"All records must have the '{key_column}' column")
            if len(record) < 2:
                raise ValueError("Records must have at least one column to update")
        
        # Process records one by one for now
        # In the future, this could be optimized with bulk operations
        results = []
        for record in records:
            update_data = {k: v for k, v in record.items() if k != key_column}
            key_value = record[key_column]
            updated = await self.update(table, update_data, {key_column: key_value})
            if updated:
                results.append(updated)
        
        return results 