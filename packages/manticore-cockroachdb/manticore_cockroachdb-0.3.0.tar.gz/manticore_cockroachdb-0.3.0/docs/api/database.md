# Database API

The `Database` class provides a synchronous interface for interacting with CockroachDB. It handles connection management, SQL execution, and transaction support.

## Class Documentation

::: manticore_cockroachdb.database.Database
    options:
      show_root_heading: true
      show_root_full_path: false
      show_source: true
      heading_level: 3
      members_order: source

## Usage Examples

```python
from manticore_cockroachdb import Database

# Connect to database
db = Database(
    host="localhost",
    port=26257,
    database="example_db",
    user="root",
    password="",
    ssl_mode="disable"
)

# Or connect using a URL
# db = Database.from_url("postgresql://root@localhost:26257/example_db?sslmode=disable")

# Create a table
db.create_table(
    "users",
    {
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "name": "TEXT NOT NULL",
        "email": "TEXT UNIQUE NOT NULL",
        "age": "INTEGER",
        "active": "BOOLEAN DEFAULT TRUE"
    },
    if_not_exists=True
)

# Insert data
user_id = db.insert("users", {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
})

# Select data
user = db.select_one("users", where={"id": user_id})
print(f"User: {user['name']}, Email: {user['email']}")

# Update data
db.update("users", {"age": 31}, where={"id": user_id})

# Delete data
db.delete("users", where={"id": user_id})

# Execute raw SQL
db.execute("SELECT * FROM users WHERE age > %s", [25])

# Use transactions
with db.transaction():
    db.insert("users", {"name": "Alice", "email": "alice@example.com", "age": 25})
    db.insert("users", {"name": "Bob", "email": "bob@example.com", "age": 28})

# Close the connection
db.close()
``` 