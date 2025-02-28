# Exceptions API

The Manticore CockroachDB client defines custom exceptions to handle specific error cases.

## Class Documentation

::: manticore_cockroachdb.crud.exceptions.TableNotInitializedError
    options:
      show_root_heading: true
      show_root_full_path: false
      show_source: true
      heading_level: 3
      members_order: source

## Usage Examples

```python
from manticore_cockroachdb import Database, Table
from manticore_cockroachdb.crud.exceptions import TableNotInitializedError

# Connect to database
db = Database(database="example_db")

# Create a Table instance without initializing
users = Table("users")

try:
    # Attempt to use the table before initializing
    user = users.create({"name": "John Doe", "email": "john@example.com"})
except TableNotInitializedError as e:
    print(f"Error: {e}")
    # Initialize the table
    users.db = db
    
# Now the table can be used
user = users.create({"name": "John Doe", "email": "john@example.com"})
print(f"Created user with ID: {user['id']}")
``` 