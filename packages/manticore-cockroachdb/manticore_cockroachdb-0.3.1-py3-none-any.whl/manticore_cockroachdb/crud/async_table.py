"""Asynchronous table management and CRUD operations."""

from typing import Dict, List, Optional, Union, Any

from ..async_database import AsyncDatabase


class AsyncTable:
    """Asynchronous database table with CRUD operations."""
    
    table_name = None
    schema = None
    
    def __init__(
        self,
        name_or_db: Union[str, AsyncDatabase],
        db: Optional[AsyncDatabase] = None,
        schema: Optional[Dict[str, str]] = None,
        if_not_exists: bool = True
    ):
        """Initialize table.
        
        Args:
            name_or_db: Table name or AsyncDatabase instance
            db: AsyncDatabase instance (if first arg is table name)
            schema: Column definitions {name: type}
            if_not_exists: Whether to create table only if it doesn't exist
        """
        # Handle different initialization patterns
        if isinstance(name_or_db, AsyncDatabase):
            self.db = name_or_db
            self.name = getattr(self, 'table_name', None)
        else:
            self.name = name_or_db
            self.db = db or AsyncDatabase()
        
        # Use schema from args or class attribute
        self._schema = schema or getattr(self, 'schema', None)
        self._if_not_exists = if_not_exists
        self._initialized = False
    
    async def initialize(self, schema: Optional[Dict[str, str]] = None, if_not_exists: bool = None) -> None:
        """Initialize the table.
        
        Args:
            schema: Column definitions {name: type}
            if_not_exists: Whether to create table only if it doesn't exist
            
        Creates the table if schema is provided and table does not exist.
        """
        if self._initialized:
            return
        
        # Use provided schema or instance schema
        schema_to_use = schema or self._schema
        if_not_exists_to_use = if_not_exists if if_not_exists is not None else self._if_not_exists
        
        if not schema_to_use:
            raise ValueError("No schema provided for table initialization")
            
        # Create table if schema is provided
        await self.db.create_table(self.name, schema_to_use, if_not_exists_to_use)
            
        self._initialized = True
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record.
        
        Args:
            data: Record data
            
        Returns:
            Created record
        """
        if not self._initialized:
            await self.initialize()
            
        return await self.db.insert(self.name, data)
    
    async def read(self, id: Union[str, int]) -> Optional[Dict[str, Any]]:
        """Read a record.
        
        Args:
            id: Record ID
            
        Returns:
            Record data or None if not found
        """
        if not self._initialized:
            await self.initialize()
            
        results = await self.db.select(self.name, where={"id": id})
        return results[0] if results else None
    
    async def update(self, id: Union[str, int], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record.
        
        Args:
            id: Record ID
            data: Update data
            
        Returns:
            Updated record
        """
        if not self._initialized:
            await self.initialize()
            
        return await self.db.update(self.name, data, {"id": id})
    
    async def delete(self, id: Union[str, int]) -> bool:
        """Delete a record.
        
        Args:
            id: Record ID
            
        Returns:
            Whether the record was deleted
        """
        if not self._initialized:
            await self.initialize()
            
        return await self.db.delete(self.name, {"id": id})
    
    async def list(
        self,
        where: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List records.
        
        Args:
            where: Filter conditions
            order_by: Order by expression
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of records
        """
        if not self._initialized:
            await self.initialize()
            
        return await self.db.select(
            self.name,
            where=where,
            order_by=order_by,
            limit=limit,
            offset=offset
        )
    
    async def count(self, where: Optional[Dict[str, Any]] = None) -> int:
        """Count records.
        
        Args:
            where: Filter conditions
            
        Returns:
            Number of records
        """
        if not self._initialized:
            await self.initialize()
            
        query = f'SELECT COUNT(*) as count FROM "{self.name}"'
        params = []
        
        if where:
            conditions = []
            for col, val in where.items():
                conditions.append(f'"{col}" = %s')
                params.append(val)
            query += f" WHERE {' AND '.join(conditions)}"
            
        result = await self.db.execute(query, tuple(params) if params else None)
        return result[0]["count"]
    
    async def batch_create(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple records in a batch.
        
        Args:
            records: Records to create
            
        Returns:
            Created records
        """
        if not self._initialized:
            await self.initialize()
            
        return await self.db.batch_insert(self.name, records)
    
    async def batch_update(
        self,
        records: List[Dict[str, Any]],
        key_column: str = "id"
    ) -> List[Dict[str, Any]]:
        """Update multiple records in a batch.
        
        Args:
            records: Records to update
            key_column: Column to use as key
            
        Returns:
            Updated records
        """
        if not self._initialized:
            await self.initialize()
            
        return await self.db.batch_update(self.name, records, key_column)
            
    async def __aenter__(self) -> 'AsyncTable':
        """Enter async context."""
        if not self._initialized:
            await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context."""
        # No need to clean up anything for the table instance
        pass 