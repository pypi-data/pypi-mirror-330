"""CockroachDB database management.

This module provides a high-level interface for managing CockroachDB databases.
"""

import logging
import os
import random
import time
from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from urllib.parse import parse_qs, urlparse

import psycopg
from psycopg.errors import SerializationFailure
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type variable for transaction return type
T = TypeVar('T')


class Transaction:
    """Database transaction context manager."""

    def __init__(self, conn: psycopg.Connection):
        """Initialize transaction.
        
        Args:
            conn: Database connection
        """
        self.conn = conn
        self._committed = False
        self._rolledback = False

    def __enter__(self) -> psycopg.Connection:
        """Enter transaction context."""
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit transaction context.
        
        Commits if no exception occurred, otherwise rolls back.
        """
        if exc_type is not None:
            if not self._rolledback:
                self.conn.rollback()
                self._rolledback = True
        else:
            if not self._committed and not self._rolledback:
                self.conn.commit()
                self._committed = True

    def commit(self) -> None:
        """Commit transaction."""
        self.conn.commit()
        self._committed = True

    def rollback(self) -> None:
        """Roll back transaction."""
        self.conn.rollback()
        self._rolledback = True


class Database:
    """Main interface for CockroachDB operations."""
    
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
        application_name: str = "manticore-db"
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
        self.connect()
    
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
    
    def connect(self) -> None:
        """Connect to database and initialize connection pool."""
        try:
            # Create connection pool
            pool = ConnectionPool(
                self.dsn,
                min_size=self.min_connections,
                max_size=self.max_connections,
                configure=lambda conn: setattr(conn, 'row_factory', dict_row),
                open=True,
                kwargs={
                    "application_name": self.application_name
                }
            )
            # Use pool as context manager
            pool.__enter__()
            self._pool = pool
            logger.info(
                f"Connected to database {self.database} "
                f"with pool size {self.min_connections}-{self.max_connections}"
            )
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def close(self) -> None:
        """Close database connection pool."""
        if self._pool:
            try:
                self._pool.__exit__(None, None, None)
            finally:
                self._pool = None
                logger.info("Closed database connection pool")
    
    def execute(
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
            raise RuntimeError("Database not connected")
            
        conn = self._pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    try:
                        results = cur.fetchall()
                        conn.commit()
                        return results
                    except psycopg.ProgrammingError:
                        # No results to fetch (e.g. for DDL statements)
                        conn.commit()
                        return None
                conn.commit()
                return None
        finally:
            self._pool.putconn(conn)
    
    def create_database(self, name: str) -> None:
        """Create a new database.
        
        Args:
            name: Database name
        """
        # Connect to default database
        default_db = Database(
            database="defaultdb",
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            sslmode=self.sslmode
        )
        
        try:
            # Check if database exists
            exists = default_db.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (name,)
            )
            
            if not exists:
                # Create database
                default_db.execute(f'CREATE DATABASE "{name}"')
                logger.info(f"Created database {name}")
            else:
                logger.info(f"Database {name} already exists")
        finally:
            default_db.close()
    
    def create_table(
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
        col_defs = [f"{col} {type_}" for col, type_ in columns.items()]
        
        # Build query
        exists_clause = "IF NOT EXISTS" if if_not_exists else ""
        query = f'CREATE TABLE {exists_clause} "{name}" ({", ".join(col_defs)})'
        
        # Execute query
        self.execute(query)
        logger.info(f"Created table {name}")
    
    def drop_table(self, name: str, if_exists: bool = True) -> None:
        """Drop a table.
        
        Args:
            name: Table name
            if_exists: Whether to drop only if table exists
        """
        exists_clause = "IF EXISTS" if if_exists else ""
        query = f'DROP TABLE {exists_clause} "{name}"'
        self.execute(query)
        logger.info(f"Dropped table {name}")
    
    def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a record into a table.
        
        Args:
            table: Table name
            data: Record data
            
        Returns:
            Inserted record
        """
        # Build query
        columns = list(data.keys())
        placeholders = [f"%s" for _ in range(len(columns))]
        values = [data[col] for col in columns]
        
        query = (
            f'INSERT INTO "{table}" ({", ".join(columns)}) '
            f'VALUES ({", ".join(placeholders)}) RETURNING *'
        )
        
        # Execute query
        results = self.execute(query, tuple(values))
        return results[0] if results else None
    
    def select(
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
        return self.execute(query, tuple(params) if params else None)
    
    def update(
        self,
        table: str,
        data: Dict[str, Any],
        where: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update records in a table.
        
        Args:
            table: Table name
            data: Update data
            where: Where conditions
            
        Returns:
            Updated record
        """
        # Build query
        updates = [f"{col} = %s" for col in data.keys()]
        conditions = [f"{col} = %s" for col in where.keys()]
        
        query = (
            f'UPDATE "{table}" SET {", ".join(updates)} '
            f'WHERE {" AND ".join(conditions)} RETURNING *'
        )
        
        # Build parameters
        params = list(data.values()) + list(where.values())
        
        # Execute query
        results = self.execute(query, tuple(params))
        return results[0] if results else None
    
    def delete(
        self,
        table: str,
        where: Dict[str, Any]
    ) -> bool:
        """Delete records from a table.
        
        Args:
            table: Table name
            where: Where conditions
            
        Returns:
            True if records were deleted, False otherwise
        """
        # First, check if record exists
        conditions = [f"{col} = %s" for col in where.keys()]
        check_query = f'SELECT COUNT(*) as count FROM "{table}" WHERE {" AND ".join(conditions)}'
        result = self.execute(check_query, tuple(where.values()))
        
        if result[0]["count"] == 0:
            return False
            
        # Build delete query
        delete_query = f'DELETE FROM "{table}" WHERE {" AND ".join(conditions)}'
        
        # Execute query
        self.execute(delete_query, tuple(where.values()), fetch=False)
        return True
    
    @classmethod
    def from_url(cls, url: str) -> 'Database':
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
        
        # We're already connecting in __init__, so no need to call connect() here
        return db
    
    def __enter__(self) -> 'Database':
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        self.close()

    def transaction(self) -> Transaction:
        """Start a new transaction.
        
        Returns:
            Transaction context manager
        """
        if not self._pool:
            raise RuntimeError("Database not connected")
            
        conn = self._pool.getconn()
        return Transaction(conn)

    def run_in_transaction(
        self,
        operation: Callable[[psycopg.Connection], T],
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
            
        conn = self._pool.getconn()
        try:
            for retry in range(max_retries):
                try:
                    with Transaction(conn) as tx_conn:
                        result = operation(tx_conn)
                        return result
                except SerializationFailure as e:
                    if retry == max_retries - 1:
                        raise ValueError(
                            f"Transaction failed after {max_retries} retries: {e}"
                        )
                    # Exponential backoff
                    sleep_ms = (2 ** retry) * 100 * (random.random() + 0.5)
                    time.sleep(sleep_ms / 1000)
                    continue
        finally:
            self._pool.putconn(conn)

    def batch_insert(
        self,
        table: str,
        records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Insert multiple records in a single transaction.
        
        Args:
            table: Table name
            records: Records to insert
            
        Returns:
            List of inserted records
        """
        if not records:
            return []
            
        # Get column names from first record
        columns = list(records[0].keys())
        
        # Build query
        placeholders = [
            f"({', '.join(['%s' for _ in range(len(columns))])})"
            for _ in range(len(records))
        ]
        query = (
            f'INSERT INTO "{table}" ({", ".join(columns)}) '
            f'VALUES {", ".join(placeholders)} '
            'RETURNING *'
        )
        
        # Flatten values
        values = [
            value
            for record in records
            for value in [record[col] for col in columns]
        ]
        
        # Execute in transaction
        def insert_batch(conn: psycopg.Connection) -> List[Dict[str, Any]]:
            with conn.cursor() as cur:
                cur.execute(query, values)
                return cur.fetchall()
                
        return self.run_in_transaction(insert_batch)

    def batch_update(
        self,
        table: str,
        records: List[Dict[str, Any]],
        key_column: str = "id"
    ) -> List[Dict[str, Any]]:
        """Update multiple records in a single transaction.
        
        Args:
            table: Table name
            records: Records to update
            key_column: Column to use as key
            
        Returns:
            List of updated records
        """
        if not records:
            return []
            
        # Get column names excluding key
        columns = [col for col in records[0].keys() if col != key_column]
        if not columns:
            raise ValueError("No columns to update")
            
        # Build SET clause
        updates = []
        values = []
        for col in columns:
            # Build CASE expression
            when_clauses = []
            for record in records:
                when_clauses.append(f"WHEN %s THEN %s")
                values.extend([record[key_column], record[col]])
            updates.append(
                f"{col} = (CASE {key_column} "
                f"{' '.join(when_clauses)} "
                f"ELSE {col} END)"
            )
            
        # Build query
        query = (
            f'UPDATE "{table}" SET {", ".join(updates)} '
            f'WHERE {key_column} IN ({", ".join(["%s" for _ in records])}) '
            f'RETURNING *'
        )
        
        # Add values for IN clause
        values.extend(record[key_column] for record in records)
        
        # Execute in transaction
        def update_batch(conn: psycopg.Connection) -> List[Dict[str, Any]]:
            with conn.cursor() as cur:
                cur.execute(query, values)
                results = cur.fetchall()
                
                # Create lookup by key
                result_map = {r[key_column]: r for r in results}
                
                # Return results in original order
                return [result_map[record[key_column]] for record in records]
                
        return self.run_in_transaction(update_batch) 