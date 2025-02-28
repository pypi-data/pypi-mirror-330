"""Table management and CRUD operations."""

from typing import Dict, List, Optional, Any

from ..database import Database


class Table:
    """Database table with CRUD operations."""
    
    def __init__(
        self,
        name: str,
        db: Optional[Database] = None,
        schema: Optional[Dict[str, str]] = None,
        if_not_exists: bool = True
    ):
        """Initialize table.
        
        Args:
            name: Table name
            db: Database instance
            schema: Column definitions {name: type}
            if_not_exists: Whether to create table only if it doesn't exist
        """
        self.name = name
        self.db = db or Database()
        
        # Initialize table schema if provided
        if schema:
            self.initialize(schema, if_not_exists)
    
    def initialize(self, schema: Dict[str, str] = None, if_not_exists: bool = True) -> None:
        """Initialize table schema.
        
        Args:
            schema: Column definitions {name: type}
            if_not_exists: Whether to create table only if it doesn't exist
        """
        if schema:
            self.db.create_table(self.name, schema, if_not_exists)
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record.
        
        Args:
            data: Record data
            
        Returns:
            Created record
        """
        return self.db.insert(self.name, data)
    
    def read(self, id: str) -> Optional[Dict[str, Any]]:
        """Read a record.
        
        Args:
            id: Record ID
            
        Returns:
            Record data or None if not found
        """
        results = self.db.select(self.name, where={"id": id})
        return results[0] if results else None
    
    def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record.
        
        Args:
            id: Record ID
            data: Update data
            
        Returns:
            Updated record
        """
        return self.db.update(self.name, data, {"id": id})
    
    def delete(self, id: str) -> bool:
        """Delete a record.
        
        Args:
            id: Record ID
            
        Returns:
            True if record was deleted
        """
        return self.db.delete(self.name, {"id": id})
    
    def list(
        self,
        where: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List records.
        
        Args:
            where: Filter conditions
            order_by: Order by clause
            limit: Result limit
            
        Returns:
            List of records
        """
        return self.db.select(
            self.name,
            where=where,
            order_by=order_by,
            limit=limit
        )
    
    def count(self, where: Optional[Dict[str, Any]] = None) -> int:
        """Count records.
        
        Args:
            where: Filter conditions
            
        Returns:
            Number of records
        """
        results = self.db.execute(
            f"SELECT COUNT(*) as count FROM {self.name}" + 
            (f" WHERE {' AND '.join(f'{k} = %s' for k in where.keys())}" if where else ""),
            tuple(where.values()) if where else None
        )
        return results[0]["count"]
    
    def batch_create(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple records.
        
        Args:
            records: Records to create
            
        Returns:
            Created records
        """
        return self.db.batch_insert(self.name, records)
    
    def batch_update(
        self,
        records: List[Dict[str, Any]],
        key_column: str = "id"
    ) -> List[Dict[str, Any]]:
        """Update multiple records.
        
        Args:
            records: Records to update
            key_column: Column to use as key
            
        Returns:
            Updated records
        """
        return self.db.batch_update(self.name, records, key_column)
    
    def __enter__(self):
        """Enter context."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        # Don't close the database here as it might be shared
        pass 