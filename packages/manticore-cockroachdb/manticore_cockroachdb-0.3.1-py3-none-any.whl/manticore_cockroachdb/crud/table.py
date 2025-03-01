"""Table management and CRUD operations."""

from typing import Dict, List, Optional, Any, Union

from ..database import Database


class Table:
    """Database table with CRUD operations."""
    
    table_name = None
    schema = None
    
    def __init__(
        self,
        name_or_db: Union[str, Database],
        db: Optional[Database] = None,
        schema: Optional[Dict[str, str]] = None,
        if_not_exists: bool = True
    ):
        """Initialize table.
        
        Args:
            name_or_db: Table name or Database instance
            db: Database instance (if first arg is table name)
            schema: Column definitions {name: type}
            if_not_exists: Whether to create table only if it doesn't exist
        """
        # Handle different initialization patterns
        if isinstance(name_or_db, Database):
            self.db = name_or_db
            self.name = getattr(self, 'table_name', None)
        else:
            self.name = name_or_db
            self.db = db or Database()
        
        # Use schema from args or class attribute
        self._schema = schema or getattr(self, 'schema', None)
        self._initialized = False
        
        # Initialize table schema if provided
        if self._schema:
            self.initialize(if_not_exists=if_not_exists)
    
    def initialize(self, schema: Optional[Dict[str, str]] = None, if_not_exists: bool = True) -> None:
        """Initialize table schema.
        
        Args:
            schema: Column definitions {name: type}
            if_not_exists: Whether to create table only if it doesn't exist
        """
        # Use provided schema or instance schema
        schema_to_use = schema or self._schema
        
        if not schema_to_use:
            raise ValueError("No schema provided for table initialization")
            
        self.db.create_table(self.name, schema_to_use, if_not_exists)
        self._initialized = True
    
    def _check_initialized(self):
        """Check if table is initialized."""
        from .exceptions import TableNotInitializedError
        if not self._initialized:
            raise TableNotInitializedError(self.name)
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record.
        
        Args:
            data: Record data
            
        Returns:
            Created record
        """
        self._check_initialized()
        return self.db.insert(self.name, data)
    
    def read(self, id: Union[str, int]) -> Optional[Dict[str, Any]]:
        """Read a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Record data
            
        Raises:
            TableNotFoundError: If the record does not exist
        """
        self._check_initialized()
        results = self.db.select(self.name, where={"id": id})
        if not results:
            from .exceptions import TableNotFoundError
            raise TableNotFoundError(f"Record with id '{id}' not found in table '{self.name}'")
        return results[0]
    
    def get(self, id: Union[str, int]) -> Optional[Dict[str, Any]]:
        """Get a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Record data or None if not found
        """
        self._check_initialized()
        results = self.db.select(self.name, where={"id": id})
        return results[0] if results else None
    
    def get_many(self, ids: List[Union[str, int]]) -> List[Dict[str, Any]]:
        """Get multiple records by their IDs.
        
        Args:
            ids: List of record IDs
            
        Returns:
            List of records matching the provided IDs
        """
        self._check_initialized()
        
        if not ids:
            return []
            
        # Build query with IN clause
        placeholders = ", ".join(["%s" for _ in ids])
        query = f'SELECT * FROM "{self.name}" WHERE "id" IN ({placeholders})'
        
        # Execute query
        return self.db.execute(query, tuple(ids)) or []
    
    def find_one(self, where: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single record by criteria.
        
        Args:
            where: Filter conditions
            
        Returns:
            Record data or None if not found
        """
        self._check_initialized()
        results = self.db.select(self.name, where=where, limit=1)
        return results[0] if results else None
    
    def update(self, id: Union[str, int], data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record by ID.
        
        Args:
            id: Record ID
            data: Update data
            
        Returns:
            Updated record
            
        Raises:
            TableNotFoundError: If the record does not exist
        """
        self._check_initialized()
        result = self.db.update(self.name, data, {"id": id})
        if result is None:
            from .exceptions import TableNotFoundError
            raise TableNotFoundError(f"Record with id '{id}' not found in table '{self.name}'")
        return result
    
    def update_where(self, where: Dict[str, Any], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update records matching criteria.
        
        Args:
            where: Filter conditions
            data: Update data
            
        Returns:
            First updated record or None if none found
        """
        self._check_initialized()
        return self.db.update(self.name, data, where)
    
    def delete(self, id: Union[str, int]) -> bool:
        """Delete a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            True if record was deleted
        """
        self._check_initialized()
        return self.db.delete(self.name, {"id": id})
    
    def delete_where(self, where: Dict[str, Any]) -> bool:
        """Delete records matching criteria.
        
        Args:
            where: Filter conditions
            
        Returns:
            True if any records were deleted
        """
        self._check_initialized()
        return self.db.delete(self.name, where)
    
    def list(
        self,
        where: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List records.
        
        Args:
            where: Filter conditions
            order_by: Order by clause
            limit: Result limit
            offset: Result offset
            
        Returns:
            List of records
        """
        self._check_initialized()
        return self.db.select(self.name, where=where, order_by=order_by, limit=limit, offset=offset)
    
    def count(self, where: Optional[Dict[str, Any]] = None) -> int:
        """Count records.
        
        Args:
            where: Filter conditions
            
        Returns:
            Number of records
        """
        self._check_initialized()
        query = f'SELECT COUNT(*) as count FROM "{self.name}"'
        params = []
        
        if where:
            conditions = []
            for col, val in where.items():
                conditions.append(f'"{col}" = %s')
                params.append(val)
            query += f" WHERE {' AND '.join(conditions)}"
        
        result = self.db.execute(query, tuple(params) if params else None)
        return result[0]["count"] if result else 0
    
    def exists(self, id: Union[str, int]) -> bool:
        """Check if a record exists by ID.
        
        Args:
            id: Record ID
            
        Returns:
            True if record exists
        """
        self._check_initialized()
        return self.count({"id": id}) > 0
    
    def batch_create(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple records.
        
        Args:
            records: Records to create
            
        Returns:
            Created records
        """
        self._check_initialized()
        return self.db.batch_insert(self.name, records)
    
    def create_many(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Alias for batch_create() - create multiple records.
        
        Args:
            records: Records to create
            
        Returns:
            Created records
        """
        return self.batch_create(records)
    
    def batch_update(
        self,
        records: List[Dict[str, Any]],
        key_column: str = "id"
    ) -> List[Dict[str, Any]]:
        """Update multiple records.
        
        Args:
            records: Records to update
            key_column: Primary key column
            
        Returns:
            Updated records
        """
        self._check_initialized()
        return self.db.batch_update(self.name, records, key_column)
    
    def update_many(
        self,
        records: List[Dict[str, Any]],
        key_column: str = "id"
    ) -> List[Dict[str, Any]]:
        """Alias for batch_update() - update multiple records.
        
        Args:
            records: Records to update
            key_column: Primary key column
            
        Returns:
            Updated records
        """
        return self.batch_update(records, key_column)
    
    def truncate(self) -> None:
        """Delete all records from the table."""
        self._check_initialized()
        self.db.execute(f'TRUNCATE TABLE "{self.name}"', fetch=False)
    
    def drop(self) -> None:
        """Drop the table."""
        self._check_initialized()
        self.db.drop_table(self.name)
    
    def execute(self, query: str, params: Optional[tuple] = None, fetch: bool = True) -> Optional[List[Dict[str, Any]]]:
        """Execute a custom SQL query on this table.
        
        Args:
            query: SQL query
            params: Query parameters
            fetch: Whether to fetch results
            
        Returns:
            Query results or None
        """
        self._check_initialized()
        return self.db.execute(query, params, fetch)
    
    def __enter__(self):
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        pass  # Database connection is managed by the Database class 