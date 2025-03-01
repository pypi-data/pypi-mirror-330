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
from psycopg.errors import SerializationFailure, UniqueViolation
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
        application_name: str = "manticore-db",
        connect_timeout: int = 30,
        connect: bool = True
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
            connect_timeout: Connection timeout in seconds
            connect: Whether to connect immediately
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
        self.connect_timeout = connect_timeout
        
        # Build connection string
        self.dsn = self._build_dsn()
        
        # Initialize connection pool
        self._pool = None
        
        # Connect to database if requested
        if connect:
            self.connect()
    
    def _build_dsn(self) -> str:
        """Build DSN string for database connection."""
        dsn = f"postgresql://{self.user}"
        if self.password:
            dsn += f":{self.password}"
        dsn += f"@{self.host}:{self.port}/{self.database}"
        dsn += f"?sslmode={self.sslmode}&application_name={self.application_name}&connect_timeout={self.connect_timeout}"
        return dsn
    
    def connect(self) -> None:
        """Connect to database."""
        if self._pool is not None:
            return
        
        try:
            dsn = self._build_dsn()
            self._pool = ConnectionPool(
                dsn,
                min_size=self.min_connections,
                max_size=self.max_connections,
                kwargs={"row_factory": dict_row}
            )
            
            # Test the connection by getting a connection from the pool
            with self._pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                
            logger.info(f"Connected to database {self.database} with pool size {self.min_connections}-{self.max_connections}")
        except Exception as e:
            from .crud.exceptions import ConnectionError
            self._pool = None
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port}", cause=e)
    
    def close(self) -> None:
        """Close database connection."""
        if self._pool is not None:
            self._pool.close()
            logger.info("Closed database connection pool")
            self._pool = None
    
    def execute(
        self,
        query: str,
        params: Optional[tuple] = None,
        fetch: bool = True
    ) -> Optional[List[Dict[str, Any]]]:
        """Execute a SQL query.
        
        Args:
            query: SQL query
            params: Query parameters
            fetch: Whether to fetch results
            
        Returns:
            Query results or None
            
        Raises:
            DatabaseError: If query execution fails
        """
        from .crud.exceptions import DatabaseError
        
        if self._pool is None:
            self.connect()
        
        conn = self._pool.getconn()
        try:
            with conn.cursor() as cur:
                try:
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
                except Exception as e:
                    conn.rollback()
                    # Wrap the exception with our DatabaseError
                    raise DatabaseError(f"Query execution failed: {str(e)}") from e
        finally:
            self._pool.putconn(conn)
    
    def create_database(self, name: str) -> None:
        """Create a new database.
        
        Args:
            name: Database name
        """
        self.execute(f'CREATE DATABASE IF NOT EXISTS "{name}"', fetch=False)
    
    def drop_database(self, name: str) -> None:
        """Drop a database.
        
        Args:
            name: Database name
        """
        self.execute(f'DROP DATABASE IF EXISTS "{name}"', fetch=False)
    
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
        exists_clause = "IF NOT EXISTS " if if_not_exists else ""
        column_defs = ", ".join([f'"{col}" {dtype}' for col, dtype in columns.items()])
        query = f'CREATE TABLE {exists_clause}"{name}" ({column_defs})'
        self.execute(query, fetch=False)
    
    def drop_table(self, name: str, if_exists: bool = True) -> None:
        """Drop a table.
        
        Args:
            name: Table name
            if_exists: Whether to drop table only if it exists
        """
        exists_clause = "IF EXISTS " if if_exists else ""
        self.execute(f'DROP TABLE {exists_clause}"{name}"', fetch=False)
    
    def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a record into a table.
        
        Args:
            table: Table name
            data: Record data
            
        Returns:
            Inserted record
        """
        from .crud.exceptions import DatabaseError
        
        # Handle empty data case
        if not data:
            query = f"""
                INSERT INTO "{table}" DEFAULT VALUES
                RETURNING *
            """
            try:
                results = self.execute(query)
                return results[0] if results else None
            except DatabaseError as e:
                # Check for unique violation
                if isinstance(e.__cause__, UniqueViolation):
                    # Re-raise with more specific message
                    constraint = str(e.__cause__).split("constraint")[1].split()[0].strip('"\'')
                    raise DatabaseError(f"Unique constraint violation: {constraint}") from e.__cause__
                raise
        
        columns = [f'"{k}"' for k in data.keys()]
        placeholders = ["%s" for _ in range(len(data))]
        values = list(data.values())
        
        query = f"""
            INSERT INTO "{table}" ({", ".join(columns)})
            VALUES ({", ".join(placeholders)})
            RETURNING *
        """
        
        try:
            results = self.execute(query, tuple(values))
            return results[0] if results else None
        except DatabaseError as e:
            # Check for unique violation
            if isinstance(e.__cause__, UniqueViolation):
                # Re-raise with more specific message
                constraint = str(e.__cause__).split("constraint")[1].split()[0].strip('"\'')
                raise DatabaseError(f"Unique constraint violation: {constraint}") from e.__cause__
            raise
    
    def select(
        self,
        table: str,
        columns: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Select records from a table.
        
        Args:
            table: Table name
            columns: Columns to select
            where: Filter conditions
            order_by: Order by clause
            limit: Result limit
            offset: Result offset
            
        Returns:
            Selected records
        """
        # Build columns clause
        if columns:
            columns_clause = ", ".join([f'"{col}"' for col in columns])
        else:
            columns_clause = "*"
        
        # Build query
        query = f'SELECT {columns_clause} FROM "{table}"'
        
        # Add where clause
        params = []
        if where:
            conditions = []
            for key in where:
                conditions.append(f'"{key}" = %s')
                params.append(where[key])
            query += f" WHERE {' AND '.join(conditions)}"
        
        # Add order by clause
        if order_by:
            query += f" ORDER BY {order_by}"
        
        # Add limit clause
        if limit:
            query += f" LIMIT {limit}"
            
        # Add offset clause
        if offset:
            query += f" OFFSET {offset}"
        
        # Execute query
        return self.execute(query, tuple(params) if params else None) or []
    
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
            where: Filter conditions
            
        Returns:
            Updated record
        """
        # Build set clause
        set_items = []
        params = []
        for i, (key, value) in enumerate(data.items()):
            set_items.append(f'"{key}" = %s')
            params.append(value)
        
        # Build where clause
        conditions = []
        for i, (key, value) in enumerate(where.items()):
            conditions.append(f'"{key}" = %s')
            params.append(value)
        
        # Build query
        query = f"""
            UPDATE "{table}"
            SET {", ".join(set_items)}
            WHERE {" AND ".join(conditions)}
            RETURNING *
        """
        
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
            where: Filter conditions
            
        Returns:
            True if records were deleted
        """
        # Build where clause
        conditions = []
        params = []
        for i, (key, value) in enumerate(where.items()):
            conditions.append(f'"{key}" = %s')
            params.append(value)
        
        # Build query
        query = f"""
            DELETE FROM "{table}"
            WHERE {" AND ".join(conditions)}
            RETURNING id
        """
        
        # Execute query
        results = self.execute(query, tuple(params))
        return bool(results)
    
    @classmethod
    def from_url(cls, url: str, connect: bool = False) -> 'Database':
        """Create database from URL.
        
        Args:
            url: Database URL in format postgresql://user:password@host:port/dbname?sslmode=mode
            connect: Whether to connect immediately
            
        Returns:
            Database instance
        """
        parsed = urlparse(url)
        
        # Extract components
        host = parsed.hostname or "localhost"
        port = parsed.port or 26257
        user = parsed.username or "root"
        password = parsed.password
        database = parsed.path.lstrip("/") or "defaultdb"
        
        # Parse query parameters
        query_params = parse_qs(parsed.query)
        sslmode = query_params.get("sslmode", ["disable"])[0]
        
        # Create database instance
        db = cls(
            database=database,
            host=host,
            port=port,
            user=user,
            password=password,
            sslmode=sslmode,
            connect=connect
        )
        
        return db
    
    def __enter__(self) -> 'Database':
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        self.close()
    
    def transaction(self) -> Transaction:
        """Create a transaction context manager.
        
        Returns:
            Transaction context manager
        """
        if self._pool is None:
            self.connect()
        
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
            max_retries: Maximum number of retries
            
        Returns:
            Operation result
        """
        from .crud.exceptions import DatabaseError
        
        if self._pool is None:
            self.connect()
        
        conn = self._pool.getconn()
        try:
            retry_count = 0
            while True:
                try:
                    with Transaction(conn) as tx:
                        return operation(tx)
                except SerializationFailure:
                    # Only retry on serialization failures
                    if retry_count >= max_retries:
                        raise DatabaseError(f"Transaction failed after {max_retries} retries")
                    
                    retry_count += 1
                    # Exponential backoff with jitter
                    delay = (0.1 * 2 ** retry_count) + (random.random() * 0.1)
                    logger.warning(f"Serialization failure, retrying in {delay:.2f}s")
                    time.sleep(delay)
                except Exception as e:
                    raise DatabaseError(f"Transaction failed: {str(e)}") from e
        finally:
            self._pool.putconn(conn)
    
    def batch_insert(
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
        for record in records[1:]:
            if set(record.keys()) != keys:
                raise ValueError("All records must have the same keys")
        
        def insert_batch(conn: psycopg.Connection) -> List[Dict[str, Any]]:
            columns = [f'"{k}"' for k in keys]
            placeholders = []
            values = []
            
            for i, record in enumerate(records):
                record_placeholders = ["%s" for _ in range(len(keys))]
                placeholders.append(f"({', '.join(record_placeholders)})")
                values.extend([record[k] for k in keys])
            
            query = f"""
                INSERT INTO "{table}" ({", ".join(columns)})
                VALUES {", ".join(placeholders)}
                RETURNING *
            """
            
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, tuple(values))
                return cur.fetchall()
        
        return self.run_in_transaction(insert_batch)
    
    def batch_update(
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
        
        # Ensure all records have the key column
        for record in records:
            if key_column not in record:
                raise ValueError(f"All records must have the key column '{key_column}'")
        
        def update_batch(conn: psycopg.Connection) -> List[Dict[str, Any]]:
            updated_records = []
            
            for record in records:
                key_value = record[key_column]
                update_data = {k: v for k, v in record.items() if k != key_column}
                
                set_items = []
                params = []
                for i, (key, value) in enumerate(update_data.items(), 1):
                    set_items.append(f'"{key}" = %s')
                    params.append(value)
                
                query = f"""
                    UPDATE "{table}"
                    SET {", ".join(set_items)}
                    WHERE "{key_column}" = %s
                    RETURNING *
                """
                params.append(key_value)
                
                with conn.cursor(row_factory=dict_row) as cur:
                    cur.execute(query, tuple(params))
                    result = cur.fetchone()
                    if result:
                        updated_records.append(result)
            
            return updated_records
        
        return self.run_in_transaction(update_batch)
    
    def exists(self, table_name: str) -> bool:
        """Check if a table exists.
        
        Args:
            table_name: Table name
            
        Returns:
            True if table exists
        """
        query = """
            SELECT COUNT(*) as count
            FROM information_schema.tables
            WHERE table_name = %s
            AND table_schema = 'public'
        """
        result = self.execute(query, (table_name,))
        return result[0]["count"] > 0 if result else False 