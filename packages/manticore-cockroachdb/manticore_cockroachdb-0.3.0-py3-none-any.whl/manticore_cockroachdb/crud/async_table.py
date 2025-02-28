"""Asynchronous table management and CRUD operations."""

from typing import Dict, List, Optional, Union

from ..async_database import AsyncDatabase


class AsyncTable:
    """Asynchronous database table with CRUD operations."""
    
    def __init__(
        self,
        name: str,
        db: Optional[AsyncDatabase] = None,
        schema: Optional[Dict[str, str]] = None,
        if_not_exists: bool = True
    ):
        """Initialize table.
        
        Args:
            name: Table name
            db: AsyncDatabase instance
            schema: Column definitions {name: type}
            if_not_exists: Whether to create table only if it doesn't exist
        """
        self.name = name
        self.db = db or AsyncDatabase()
        self.schema = schema
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the table.
        
        Creates the table if schema is provided and table does not exist.
        """
        if self._initialized:
            return
            
        # Create table if schema is provided
        if self.schema:
            await self.db.create_table(self.name, self.schema, True)
            
        self._initialized = True
    
    async def create(self, data: Dict) -> Dict:
        """Create a new record.
        
        Args:
            data: Record data
            
        Returns:
            Created record
        """
        if not self._initialized:
            await self.initialize()
            
        return await self.db.insert(self.name, data)
    
    async def read(self, id: Union[str, int]) -> Optional[Dict]:
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
    
    async def update(self, id: Union[str, int], data: Dict) -> Optional[Dict]:
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
        where: Optional[Dict] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """List records.
        
        Args:
            where: Filter conditions
            order_by: Order by expression
            limit: Maximum number of records to return
            
        Returns:
            List of records
        """
        if not self._initialized:
            await self.initialize()
            
        return await self.db.select(
            self.name,
            where=where,
            order_by=order_by,
            limit=limit
        )
    
    async def count(self, where: Optional[Dict] = None) -> int:
        """Count records.
        
        Args:
            where: Filter conditions
            
        Returns:
            Number of records
        """
        if not self._initialized:
            await self.initialize()
            
        query = f"SELECT COUNT(*) as count FROM {self.name}"
        params = []
        
        if where:
            conditions = []
            for key, value in where.items():
                conditions.append(f"{key} = %s")
                params.append(value)
            query += f" WHERE {' AND '.join(conditions)}"
            
        result = await self.db.execute(query, tuple(params))
        return result[0]["count"]
    
    async def batch_create(self, records: List[Dict]) -> List[Dict]:
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
        records: List[Dict],
        key_column: str = "id"
    ) -> List[Dict]:
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